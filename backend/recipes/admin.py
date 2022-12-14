from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    NumberOfIngredients,
    Recipe,
    ShoppingCart,
    Tag
)


EMPTY_VALUE = '-пусто-'


class RecipeIngredientsAdmin(admin.ModelAdmin):
    model = NumberOfIngredients,
    autocomplete_fields = ('ingredients',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'text',
        'cooking_time',
        'pub_date',
        'get_favorite_count'
    )
    search_fields = (
        'name',
        'cooking_time',
        'author__username',
        'ingredients__name'
    )
    list_filter = ('pub_date', 'tags',)
    empty_value_display = EMPTY_VALUE

    @admin.display(description='В избранном')
    def get_favorite_count(self, obj):
        return obj.favorite.count()


@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    empty_value_display = EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    empty_value_display = EMPTY_VALUE
