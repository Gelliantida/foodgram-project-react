'''Создание view-классов.'''

from http import HTTPStatus

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AdminOrAuthor, AdminOrReadOnly
from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    Favorite,
    ShoppingBasket,
    NumberOfIngredients
)
from .serializers import (
    CommonIngredientSerializer,
    FollowSerializer,
    RecipeFollowSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer,
    UserFollowSerializer,
)
from users.models import User, Follow


SHOPPING_LIST_NAME = 'shopping_list.txt'


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserFollowSerializer
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                Follow.objects.create(
                    user=request.user,
                    author=author
                ), context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        Follow.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = CommonIngredientSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AdminOrAuthor,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def __add_recipe(model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(recipe=recipe, user=request.user)
        serializer = RecipeFollowSerializer(recipe)
        return Response(data=serializer.data, status=HTTPStatus.CREATED)

    @staticmethod
    def __delete_recipe(model, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.__add_recipe(Favorite, request, pk)
        return self.__delete_recipe(Favorite, request, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def recipe(self, request, pk):
        if request.method == 'POST':
            return self.__add_recipe(Recipe, request, pk)
        return self.__delete_recipe(Recipe, request, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_basket(self, request, pk):
        if request.method == 'POST':
            return self.__add_recipe(ShoppingBasket, request, pk)
        return self.__delete_recipe(ShoppingBasket, request, pk)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_basket.exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        ingredients = NumberOfIngredients.objects.filter(
            recipe__shopping_basket__user=user
        ).values(
            'ingredients__name',
            'ingredients__measurement_unit',
        ).annotate(
            value=Sum('amount')
        ).order_by('ingredients__name')
        response = HttpResponse(
            content_type='text/plain',
            charset='utf-8',
        )
        response['Content-Disposition'] = (
            f'attachment; filename={SHOPPING_LIST_NAME}'
        )
        response.write('Список продуктов к покупке:\n')
        for ingredient in ingredients:
            response.write(
                f'- {ingredient["ingredients__name"]} '
                f'- {ingredient["value"]} '
                f'{ingredient["ingredients__measurement_unit"]}\n'
            )
        return response
