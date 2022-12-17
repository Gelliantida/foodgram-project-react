"""Создание фильтров."""

from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    """Фильтр для ингридиентов."""

    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов."""

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_basket = filters.BooleanFilter(
        field_name='is_in_shopping_basket',
        method='shopping_basket_filter'
    )

    def favorite_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_favorited."""

        return Recipe.objects.filter(favorite__user=self.request.user)

    def shopping_basket_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_in_shopping_basket."""

        return Recipe.objects.filter(shopping_basket__user=self.request.user)

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Recipe
        fields = ['author']
