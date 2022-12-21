from django.contrib.admin import ModelAdmin, TabularInline, register
from django.utils.safestring import mark_safe

from .models import Ingredient, QuantityOfIngredients, Recipe, Tag

ModelAdmin.empty_value_display = '-пусто-'


class QuantityOfIngredientsInline(TabularInline):
    model = QuantityOfIngredients
    ordering = ('ingredient',)
    autocomplete_fields = ('ingredient',)
    extra = 1


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    ordering = ('name',)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'cnt_fav', 'cnt_shop')
    fields = (
        ('name', 'cooking_time'), 'author', 'tag',
        'text', 'image', 'preview'
    )
    search_fields = ('name', 'author')
    list_filter = ('author__username', 'name', 'tag__name')
    readonly_fields = ('preview',)
    raw_id_fields = ('author',)
    inlines = (QuantityOfIngredientsInline,)
    filter_horizontal = ('tag',)

    def preview(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px">'
        )

    def cnt_fav(self, obj):
        return obj.favorite.count()
    cnt_fav.short_description = 'В избранном'

    def cnt_shop(self, obj):
        return obj.purchase.count()
    cnt_shop.short_description = 'В корзине'
