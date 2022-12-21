from api.helpers import Helper
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, QuantityOfIngredients, Recipe, Tag
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField, ValidationError)
from users.serializers import CustomUserSerializer


class TagSerializer(ModelSerializer):
    """Сериализатор для информации о тегах"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    """Сериализатор для информации об ингредиентах"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class QuantityOfIngredientsSerializer(ModelSerializer):
    """Сериализатор для вывода информации об ингредиентах в рецептах."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = QuantityOfIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer, Helper):
    """Сериализатор для вывода информации о рецептах."""
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(source='tag', many=True, read_only=True)
    ingredients = QuantityOfIngredientsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        """Метод проверяет находится ли рецепт в избранном."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites_recipes.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод проверяет находится ли рецепт в списке покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.purchases.filter(id=obj.id).exists()

    def validate(self, data):
        """Проверяет данные, введённые юзером при создании/обновлении рецепта.

        Проверяемое поле - «ingredients»:
            - проверяет чтобы присутствовал хотя-бы 1 ингредиент
            - проверяет чтобы не было повторяющихся ингредиентов
            - проверяет чтобы значение «amount» было больше 0
        Проверяемое поле - «tags»:
            - проверяет чтобы присутствовал хотя-бы 1 тег
        """
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not tags:
            raise ValidationError(
                {'tags': 'Убедитесь, что добавили хотя-бы 1 тег'}
            )
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Убедитесь, что добавили хотя-бы 1 ингредиент'}
            )
        errors = list()
        added_ingredients = list()
        try:
            for ingredient in ingredients:
                if int(ingredient['amount']) < 1:
                    errors.append(
                        'Убедитесь, что в поле amount указано число больше 0'
                    )
                elif ingredient['id'] in added_ingredients:
                    errors.append(
                        'Убедитесь, что не добавили одинаковые ингредиенты'
                    )
                added_ingredients.append(ingredient['id'])
        except KeyError:
            raise ValidationError(
                {'ingredients': 'Убедитесь, что правильно назвали поля '
                                'для обозначения ингредиента'}
            )
        if errors:
            raise ValidationError({'ingredients': errors})
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Метод для создания рецепта.

        Необходимые данные:
            - ingredients: список ингредиентов, с указанием «id» и «amount»
            - tags: список id тегов
            - image: картинка, закодированная в Base64
            - name: название
            - text": описание рецепта
            - cooking_time: время приготовления (в минутах)
        """
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tag.set(tags_data)
        self.create_or_update_ingredients(recipe, ingredients_data)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        """Метод для обновления рецепта."""
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time
        )
        recipe.tag.clear()
        recipe.tag.set(validated_data.pop('tags'))
        QuantityOfIngredients.objects.filter(recipe=recipe).delete()
        ingredients_data = validated_data.pop('ingredients')
        self.create_or_update_ingredients(recipe, ingredients_data)
        recipe.save()
        return recipe
