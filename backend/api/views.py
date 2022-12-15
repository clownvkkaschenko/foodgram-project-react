from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


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


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(methods=['POST', 'DELETE'], pagination_class=None, detail=True)
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(self.queryset, id=pk)
        serializer = FavoriteSerializer(recipe, context={'request': request})
        validate_recipe = user.favorites_recipes.filter(id=pk).exists()

        if request.method == 'POST' and not validate_recipe:
            user.favorites_recipes.add(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)
        elif request.method == 'DELETE' and validate_recipe:
            user.favorites_recipes.remove(recipe)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
