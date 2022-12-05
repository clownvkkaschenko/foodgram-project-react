"""Файл для проектирования и описания моделей приложения 'recipes' для ORM.

Модели:
    - Ingredient:
        Модель для описания ингредиентов.
    - Tag:
        Модель тегов для рецептов.
    - Recipe:
        Основная модель приложения, для создания и описания рецептов.
    - QuantityOfIngredients:
        Промежуточная модель количества ингредиентов в блюде.
    - Subscription:
        Модель подписки на пользователей.
"""

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()

MAX_LENGTH_HEX_CODE = 6
MAX_LENGTH_CHARFIELD = 256
MAX_LENGTH_TEXTFIELD = 2000
MIN_VALUE_INTEGERFIELD = 1


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Название продукта'
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Теги для рецептов."""
    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD, unique=True,
        verbose_name='Название тега'
    )
    color_code = models.CharField(
        max_length=MAX_LENGTH_HEX_CODE, unique=True, verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_CHARFIELD, unique=True,
        verbose_name='Адрес тега'
    )


class Recipe(models.Model):
    """Модель создания рецептов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
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
        User, related_name='favorites_recipes',
        verbose_name='Избранные рецепты'
    )
    purchase = models.ManyToManyField(
        User, related_name='purchases',
        verbose_name='Список покупок'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Дата публикации'
    )

    class Meta:
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
                fields=('ingredient', 'recipe'), name='unique_object'
            )
        ]
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Модель подписки на пользователей."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followers', verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор на которого подписываются'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_object'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        def __str__(self):
            return self.name
