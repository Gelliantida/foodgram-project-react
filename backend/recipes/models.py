"""Создание моделей."""

from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


INGREDIENT_NAME_LENGTH = 200
MEASUREMENT_UNIT_LENGTH = 25
TAG_NAME_LENGTH = 50
TAG_COLOR_LENGTH = 10
TAG_SLUG_LENGTH = 50
RECIPE_NAME_LENGTH = 200
COCKING_TIME_MESSAGE = 'Время приготовления не может быть менее 1 минуты'
NUMBER_OF_INGREDIENTS = ('Минимальное колличество ингредиентов не может быть'
                         ' меньше 1')


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=INGREDIENT_NAME_LENGTH,
        blank=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MEASUREMENT_UNIT_LENGTH,
        blank=False,
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ['id', ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=TAG_NAME_LENGTH,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        unique=True,
        max_length=TAG_COLOR_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=TAG_SLUG_LENGTH
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ['id', ]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:20]


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
        verbose_name='Название рецепта',
        max_length=RECIPE_NAME_LENGTH
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='NumberOfIngredients',
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
        verbose_name='Время приготовления (минуты)',
        validators=[
            MinValueValidator(
                1, message=COCKING_TIME_MESSAGE
            ),
        ],
        null=True
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/',
    )
    text = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        """Дополнительные параметры модели."""

        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:20]


class NumberOfIngredients(models.Model):
    """Модель числа ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='amount_ingredients'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='amount_ingredients'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Число ингредиентов',
        validators=[
            MinValueValidator(
                1, message=NUMBER_OF_INGREDIENTS
            ),
        ]
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
        return f'В {self.recipe} {self.amount} {self.ingredients}'


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


class ShoppingCart(models.Model):
    """Модель корзины покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        """Дополнительные параметры модели."""

        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe', ],
                name='unique_shopping_cart'
            ),
        ]

    def __str__(self):
        return f'Список покупок {self.user}.'
