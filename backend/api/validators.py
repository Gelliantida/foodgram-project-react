'''Валидаторы для сериализатора рецептов'''

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Ingredient


class RecipeValidator:
    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 мин.'
            )
        return cooking_time

    def validate_ingredients(self, data):
        ingredients = data.get('ingredients')
        validated_items = []
        existed = []
        for item in data:
            ingredient = get_object_or_404(Ingredient, pk=item['id'])
            if ingredient in validated_items:
                existed.append(ingredient)
            validated_items.append(ingredient)
        if existed:
            raise serializers.ValidationError(
                'Этот ингредиент уже добавлен'
            )
        data['ingredients'] = ingredients
        return data
