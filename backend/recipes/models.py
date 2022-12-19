"""Файл для проектирования и описания моделей приложения «recipes» для ORM.

Модели:
  - Ingredient(строка-19): Модель ингредиентов и их единицы измерения.
  - Tag(строка-48): Модель тегов для рецептов.
  - Recipe(строка-77): Основная модель приложения, для создания и
                       описания рецептов.
  - QuantityOfIngredients(строка-146): Промежуточная модель количества
                                       ингредиентов в блюде.
"""
from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from foodgram.constants import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_HEX_CODE,
                                MAX_LENGTH_NAME_RECIPE, MAX_LENGTH_TEXTFIELD,
                                MIN_VALUE_INTEGERFIELD)
from users.models import CustomUser


class Ingredient(models.Model):
    """Модель ингредиентов и их единиц измерений.

    Поля модели(являются обязательными):
      - name: название ингредиента
      - measurement_unit: единица измерения ингредиента
    """
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Название продукта'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Единица измерения продукта'
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
    """Модель тегов для рецептов.

    Поля модели(являются обязательными):
      - name: название тега
      - color: цвет тега
      - slug: уникальный фрагмент URL-адреса для тега
    """
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
        verbose_name='URL-адрес тега'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Основная модель приложения, для создания и описания рецептов.

    Поля модели(являются обязательными):
      - author(1:М с моделью «CustomUser»): автор рецепта
      - name: название блюда
      - image: фото блюда
      - text: описание рецепта
      - ingredient(M2M с моделью «Ingredient»): продукты для приготовления
                                                блюда
      - tag(M2M с моделью «Tag»): теги рецепта
      - cooking_time: время готовки блюда(в минутах)
      - favorite(M2M с моделью «CustomUser»): избранные рецепты
      - purchase(M2M с моделью «CustomUser»): список покупок для
                                              выбранных рецептов
    """
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор публикации'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_RECIPE, verbose_name='Название блюда'
    )
    image = models.ImageField(
        upload_to='recipes/', verbose_name='Фотография блюда'
    )
    text = models.TextField(
        max_length=MAX_LENGTH_TEXTFIELD,
        verbose_name='Текстовое описание рецепта'
    )
    ingredient = models.ManyToManyField(
        Ingredient, through='QuantityOfIngredients',
        related_name='recipes', verbose_name='Ингредиенты для блюда'
    )
    tag = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления блюда(в минутах)',
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
    Поля модели:
      - ingredient(1:M с моделью «Ingredient»): ингредиенты для блюда
      - recipe(1:M с моделью «Recipe»): рецепт блюда
      - amount: количество ингридиентов в блюде
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
        verbose_name='Количество ингредиентов',
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
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}шт. для {self.recipe}'
