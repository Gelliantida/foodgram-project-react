"""Создание фильтров."""

import django_filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для ингридиентов."""

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецептов."""

    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_basket = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_favorited."""

        return Recipe.objects.filter(favorite__user=self.request.user)

    def shopping_cart_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_in_shopping_basket."""

        return Recipe.objects.filter(shopping_cart__user=self.request.user)

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Recipe
        fields = ['author']
