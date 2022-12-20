"""Создание фильтров."""

from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


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

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    author = filters.NumberFilter(field_name='author__id')
    is_favorited = filters.BooleanFilter(
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_favorited."""

        return Recipe.objects.filter(favorite__user=self.request.user)

    def shopping_cart_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_in_shopping_cart."""

        return Recipe.objects.filter(shopping_cart__user=self.request.user)

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Recipe
        fields = ('tags','author')
