from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, QuantityOfIngredients, Recipe, Tag
from rest_framework import serializers
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False
        return user.subscriber.filter(id=obj.id).exists()


class CustomUserRegistrationSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class QuantityOfIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = QuantityOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(source='tag', many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = QuantityOfIngredientsSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites_recipes.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.purchases.filter(id=obj.id).exists()

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tag.set(tags_data)
        for ingredient_data in ingredients_data:
            QuantityOfIngredients.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount')
            )
        return recipe

    def update(self, recipe, validated_data):
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('name', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )
        if self.initial_data.get('tags'):
            recipe.tag.clear()
            recipe.tag.set(self.initial_data.get('tags'))

        if self.initial_data.get('ingredients'):
            QuantityOfIngredients.objects.filter(recipe=recipe).all().delete()

            ingredients_data = self.initial_data.get('ingredients')
            for ingredient_data in ingredients_data:
                QuantityOfIngredients.objects.create(
                    recipe=recipe,
                    ingredient_id=ingredient_data.get('id'),
                    amount=ingredient_data.get('amount')
                )
        recipe.save()
        return recipe
