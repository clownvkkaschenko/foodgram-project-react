from django.db.models import F, Sum
from django.http import HttpResponse
from djoser.views import UserViewSet
from recipes.models import Ingredient, QuantityOfIngredients, Recipe, Tag
from recipes.serializers import (IngredientSerializer, RecipeSerializer,
                                 TagSerializer)
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.serializers import (FavoriteAndPurchaseSerializer,
                               SubscribeSerializer)

from .helpers import Helper
from .paginations import PageNumberLimitPagination
from .permissions import IsOwnerOrReadonlyPermission


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class SubscribeUserViewSet(UserViewSet, Helper):
    queryset = CustomUser.objects.all()
    additional_serializer = SubscribeSerializer

    @action(methods=['GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        """Метод выводит список пользователей, на которых есть подписка."""
        user = request.user
        queryset = user.subscribers.all()
        page = self.paginate_queryset(queryset)
        serializer = self.additional_serializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,), detail=True)
    def subscribe(self, request, id):
        """Метод для подписки/отписки от пользователя."""
        return self.post_or_delete(id, request.user.subscribers)


class RecipeViewSet(viewsets.ModelViewSet, Helper):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadonlyPermission,)
    pagination_class = PageNumberLimitPagination
    additional_serializer = FavoriteAndPurchaseSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tag__slug__in=tags).distinct()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        user = self.request.user
        if user.is_anonymous:
            return queryset
        query = [
            {
                '1': queryset.filter(favorite=user.id),
                '0': queryset.exclude(favorite=user.id)
            },
            {
                '1': queryset.filter(purchase=user.id),
                '0': queryset.exclude(purchase=user.id)
            }
        ]
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        if is_favorited:
            queryset = query[0][is_favorited]
        elif is_in_shopping_cart:
            queryset = query[1][is_in_shopping_cart]
        return queryset

    @action(methods=['POST', 'DELETE'], pagination_class=None,
            permission_classes=(IsAuthenticated,), detail=True)
    def favorite(self, request, pk):
        """Метод для добавления/удаления рецепта из избранного."""
        return self.post_or_delete(pk, request.user.favorites_recipes)

    @action(methods=['POST', 'DELETE'], pagination_class=None,
            permission_classes=(IsAuthenticated,), detail=True)
    def shopping_cart(self, request, pk):
        """Метод для добавления/удаления рецепта из списка покупок."""
        return self.post_or_delete(pk, request.user.purchases)

    @action(methods=['GET'], detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Метод для загрузки списка покупок пользователя в формате txt."""
        user = request.user
        ingredients = QuantityOfIngredients.objects.filter(
            recipe__in=(user.purchases.values('id'))
        ).values(
            ingredients=F('ingredient__name'),
            measurement=F('ingredient__measurement_unit')
        ).annotate(
            amount=Sum('amount')
        )

        purchases = list()
        for ingredient in ingredients:
            purchases += (
                f'{ingredient["ingredients"]}: '
                f'{ingredient["amount"]} {ingredient["measurement"]}\n'
            )
        response = HttpResponse(purchases, content_type='text.txt')
        filename = 'Spisok_pokupok.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
