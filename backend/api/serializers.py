"""Создание сериализаторов."""

from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    NUMBER_OF_INGREDIENTS,
    Ingredient,
    Favorite,
    NumberOfIngredients,
    Recipe,
    ShoppingBasket,
    Tag
)
from users.models import Follow, User

from .validators import RecipeValidator


class CreateUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'username',
        )
        extra_kwargs = {'password': {'write_only': True}}


class UserFollowSerializer(UserSerializer):
    """Сериализатор для проверки подписок."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Follow.objects.filter(
            user=user, author=obj
        ).exists() if user.is_authenticated else False


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор управления моделью тэг"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class CommonIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для управления ингридиентами"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов для рецептов."""

    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit'
    )

    class Meta:
        model = NumberOfIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'number',
        )
        validators = [UniqueTogetherValidator(
            queryset=NumberOfIngredients.objects.all(),
            fields=['ingredient', 'recipe'])]


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиентов в рецепт."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = NumberOfIngredients
        fields = ('id', 'number')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(NUMBER_OF_INGREDIENTS)
        return value


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для обработки рецептов."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_basket = serializers.SerializerMethodField()
    author = UserFollowSerializer(read_only=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField(use_url=True, )
    ingredients = IngredientReadSerializer(
        many=True,
        source='number_ingredients',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_basket',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return Favorite.objects.filter(
            user=user, recipe=obj
        ).exists() if all(
            [user.is_authenticated, self.context.get('request') is not None]
        ) else False

    def get_is_in_shopping_basket(self, obj):
        user = self.context.get('request').user
        return ShoppingBasket.objects.filter(
            user=user, recipe=obj
        ).exists() if user.is_authenticated else False


class RecipeWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецептов.
    Методы валидации описаны в классе RecipeValidator.
    """

    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(use_url=True, )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

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

    @staticmethod
    def add_ingredients(ingredients, recipe):
        ingredient_list = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            recipe_ingredient = NumberOfIngredients(
                ingredients=get_object_or_404(
                    Ingredient, id=ingredient['id']
                ),
                recipe=recipe,
                amount=amount
            )
            ingredient_list.append(recipe_ingredient)
        NumberOfIngredients.objects.bulk_create(ingredient_list)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        self.add_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        NumberOfIngredients.objects.filter(recipe=recipe).delete()
        self.add_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, recipe):
        return RecipeReadSerializer(
            recipe,
            context={'request': self.context.get('request')}
        ).data


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта в подписке."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeFollowSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    @staticmethod
    def get_is_subscribed(self, obj):
        return Follow.objects.filter(user=obj.user, author=obj.author).exists()
