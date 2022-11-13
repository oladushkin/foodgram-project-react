from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (
    APITagList, APIIngredientList, FavoriteViewSet,
    RecipeViewSet, APIShopping, download_shopping_list
)

router_v1 = SimpleRouter()
router_v1.register(
    'tags',
    APITagList
)
router_v1.register(
    'ingredients',
    APIIngredientList
)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite',
    FavoriteViewSet
)
router_v1.register(
    'recipes',
    RecipeViewSet
)
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    APIShopping
)
urlpatterns = [
    path('', include(router_v1.urls)),
    path('recipes/download_shopping_cart', download_shopping_list)
]
