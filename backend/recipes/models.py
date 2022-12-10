"""Файл для проектирования и описания моделей приложения 'recipes' для ORM.

Модели:
    - Ingredient(line-21):
            Модель для описания ингредиентов.
    - Tag(line-44):
            Модель тегов для рецептов.
    - Recipe(line-67):
            Основная модель приложения, для создания и описания рецептов.
    - QuantityOfIngredients(line-125):
            Промежуточная модель количества ингредиентов в блюде.
"""
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from foodgram.constant import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_HEX_CODE,
                               MAX_LENGTH_TEXTFIELD, MIN_VALUE_INTEGERFIELD)
from users.models import CustomUser


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Название продукта'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Единица измерения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='%(app_label)s_%(class)s_unique_object'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}({self.measurement_unit})'


class Tag(models.Model):
    """Теги для рецептов."""
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, unique=True,
        verbose_name='Название тега'
    )
    color = ColorField(
        max_length=MAX_LENGTH_HEX_CODE, unique=True,
        default='#000000', verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_CHARFIELD, unique=True,
        verbose_name='Адрес тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель создания рецептов."""
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Название блюда'
    )
    image = models.ImageField(
        upload_to='recipes/', verbose_name='Фотография блюда'
    )
    description = models.TextField(
        max_length=MAX_LENGTH_TEXTFIELD, verbose_name='Текстовое описание'
    )
    ingredient = models.ManyToManyField(
        Ingredient, through='QuantityOfIngredients',
        related_name='recipes', verbose_name='Ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления(в минутах)',
        validators=[
            MinValueValidator(
                MIN_VALUE_INTEGERFIELD,
                message='Минимальное время приготовления - 1 минута'
            )
        ]
    )
    favorite = models.ManyToManyField(
        CustomUser, related_name='favorites_recipes',
        verbose_name='Избранные рецепты'
    )
    purchase = models.ManyToManyField(
        CustomUser, related_name='purchases',
        verbose_name='Список покупок'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='%(app_label)s_%(class)s_unique_recipe_name'
            )
        ]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class QuantityOfIngredients(models.Model):
    """Промежуточная модель количества ингредиентов в блюде.

    Имеет отношение «one-to-many» с моделями «Ingredient» и «Recipe».
    И определяет одно дополнительное поле «amount».
    """
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredients', verbose_name='Ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredients', verbose_name='Рецепты'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингридиентов',
        validators=[
            MinValueValidator(
                MIN_VALUE_INTEGERFIELD,
                message='Минимальное количество - 1'
            )
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='%(app_label)s_%(class)s_unique_ingredient'
            )
        ]
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}шт. для {self.recipe}'
