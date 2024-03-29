from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIIngredientList, APIShopping, APITagList,
                    DownloadShoppingCartView, FavoriteViewSet, RecipeViewSet)

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
    r'recipes/(?P<recipe_id>\d+)/shopping_cart',
    APIShopping
)
router_v1.register(
    'recipes',
    RecipeViewSet
)
urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCartView.as_view(),
        name='download_shopping_cart'
    ),
    path('', include(router_v1.urls)),
]
