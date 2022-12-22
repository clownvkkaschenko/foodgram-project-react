from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import CustomUser


class CustomUserRegistrationSerializer(UserCreateSerializer):
    """Сериализатор для регистрации новых пользователей."""

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """Сериализатор для вывода информации о пользователях."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        """Метод проверяет, находится ли пользователь в подписках."""
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False
        return user.subscribers.filter(id=obj.id).exists()


class FavoriteAndPurchaseSerializer(ModelSerializer):
    """Укороченный сериализатор рецепта.

    Для вывода информации о рецепте, при его добавлении в избранное или
    в список покупок. А так же для вывода информации о рецептах пользователя
    при подписке на него.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    """Сериализатор для информации о юзерах на которых оформлена подписка."""
    is_subscribed = SerializerMethodField()
    recipes_count = SerializerMethodField()
    recipes = FavoriteAndPurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        """Метод считает количество рецептов пользователя."""
        return obj.recipes.count()
