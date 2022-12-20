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
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        label="Tags",
        to_field_name="slug",
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='favorite_filter'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_favorited."""

        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__author=self.request.user)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        """Функция обработки пременной get_is_in_shopping_cart."""

        return Recipe.objects.filter(shopping_cart__user=self.request.user)

    class Meta:
        """Дополнительные параметры фильтра."""

        model = Recipe
        fields = ['author']
