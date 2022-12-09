"""Создание моделей."""

from django.db import models
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=25,
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    color = models.CharField(
        verbose_name='Цвет',
        unique=True,
        max_length=20
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=50
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        null=True
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (минуты)'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media'
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=500
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}'


class NumberOfIngredients(models.Model):
    """Модель числа ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='number_ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='number_ingredients'
    )
    number = models.PositiveIntegerField(
        verbose_name='Число ингредиентов'
    )

    class Meta:
        """Дополнительные параметры модели."""

        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredients', 'recipe',),
                name='recipe_ingredient_constraint'
            )
        ]

    def __str__(self):
        return f'В {self.recipe} {self.number} {self.ingredients}'


class Favorite(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт',
        related_name='favorite'
    )

    class Meta:
        """Дополнительные параметры модели."""

        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_user_recipe',
            ),
        ]

    def __str__(self):
        return f'{self.recipe} добавлен в избранные {self.user}'


class ShoppingBasket(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_basket',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_basket',
    )

    class Meta:
        """Дополнительные параметры модели."""

        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe',
                ],
                name='unique_shopping_basket')
        ]

    def __str__(self):
        return f'Список покупок {self.user}.'