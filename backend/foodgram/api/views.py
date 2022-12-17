from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingList, Tag
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, POST_RecipeSerializer,
                          ShoppingSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вывод рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    def get_serializer_class(self):
        if (hasattr(self, 'action') and self.action == 'create') or \
           self.request.method == 'PATCH':
            return POST_RecipeSerializer
        return RecipeSerializer

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(RecipeViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(RecipeViewSet, self).perform_destroy(instance)


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Избранные рецепты"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        user = self.request.user
        serializer.save(recipe=recipe, user=user)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        favorite = get_object_or_404(Favorite, recipe=recipe.id, user=user.id)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APITagList(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Теги"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class APIIngredientList(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Ингридиенты"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class APIShopping(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Список рецептов добавленных в корзину"""
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        user = self.request.user
        serializer.save(recipe=recipe, user=user)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user = request.user
        favorite = get_object_or_404(
            ShoppingList,
            recipe=recipe.id,
            user=user.id
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(APIView):
    """Скачивание списка покупок."""
    def get(self, request):
        shopping_list = ShoppingList.objects.filter(user=request.user)
        shop_list = {}

        for shopp in shopping_list:
            recipe = get_object_or_404(Recipe, pk=shopp.recipe.id)
            ingredients = recipe.ingredients_recipe.all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                if name in shop_list.keys():
                    shop_list[name]['amount'] += ingredient.amount
                else:
                    shop_list[name] = {
                        'amount': ingredient.amount,
                        'measurement_unit':
                        ingredient.ingredient.measurement_unit
                        }

        lines = []
        for line in shop_list.keys():
            lines.append(
                (f"{line} - {shop_list[line]['amount']}"
                 f" {shop_list[line]['measurement_unit']}")
            )

        # Шаблон текстового файла
        buffer = open('shop_list.txt', 'wb+')
        buffer.write('Продуктовый помошник.'.encode())
        buffer.write('\n'.encode())
        buffer.write('Список покупок'.encode())
        buffer.write('\n'.encode())
        for line in lines:
            buffer.write(line.encode())
            buffer.write('\n'.encode())
        buffer.write('Удачных покупок'.encode())
        buffer.seek(0)
        # Конец шаблона
        return FileResponse(
            buffer,
            as_attachment=True,
            filename='shop_list.txt'
            )
