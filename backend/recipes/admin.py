from django.contrib.admin import ModelAdmin, TabularInline, register
from django.utils.safestring import mark_safe

from .models import Ingredient, QuantityOfIngredients, Recipe, Tag

ModelAdmin.empty_value_display = '-пусто-'


class QuantityOfIngredientsInline(TabularInline):
    model = QuantityOfIngredients
    autocomplete_fields = ('ingredient',)
    extra = 1


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('id', 'name', 'author', 'cnt_favorites', 'get_image')
    fields = (
        ('name', 'cooking_time'), 'author', 'tag',
        'description', 'image'
    )
    raw_id_fields = ('author',)
    search_fields = ('name', 'author')
    list_filter = ('author__username', 'name', 'tag__name')
    inlines = (QuantityOfIngredientsInline,)
    filter_horizontal = ('tag',)

    def get_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="width: 100px; hieght: 50px;">'
        )
    get_image.short_description = 'Изображение'

    def cnt_favorites(self, obj):
        return obj.favorite.count()
    cnt_favorites.short_description = 'В избранном'
