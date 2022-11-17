import io
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from django.http import FileResponse
from .serializers import (
    RecipeSerializer, FavoriteSerializer,
    TagSerializer, IngredientSerializer,
    ShoppingSerializer
)
from recipes.models import Recipe, Favorite, Tag, Ingredient, ShoppingList


class RecipeViewSet(viewsets.ModelViewSet):
    """Рецепты"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(RecipeViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(RecipeViewSet, self).perform_destroy(instance)


class FavoriteViewSet(viewsets.ModelViewSet):
    """Избранные рецепты"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class APITagList(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet
):
    """Теги"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class APIIngredientList(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet
):
    """Ингридиенты"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class APIShopping(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Список рецептов добавленных в корзину"""
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingSerializer


@api_view(['GET', ])
def download_shopping_list(request):
    shopping_list = ShoppingList.objects.filter(user=request.user)
    shop_list = {}
    for recipe in shopping_list:
        list_ingredient = recipe.ingredient
        for ingredient in list_ingredient:
            if ingredient.ingredient.name in shop_list:
                shop_list[ingredient.ingredient.name] = shop_list[ingredient.ingredient.name]['amount'] + ingredient.amount
            shop_list[ingredient.ingredient.name] = {'amount':ingredient.amount, 'measurement_unit':ingredient.ingredient.measurement_unit}

    buffer = io.StringIO()
    for line in shop_list.keys():
        buffer.write(f"{shop_list[line]} - {shop_list[line]['amount']} {shop_list[line]['measurement_unit']}\n")
    return FileResponse(buffer, as_attachment=True, filename='shop_list.txt')
