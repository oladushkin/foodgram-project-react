from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from .views import APIFollowList, UserViewSet

app_name = 'users'

router = SimpleRouter()
router.register(
    'follow',
    APIFollowList
)
router.register(
    'users',
    UserViewSet
)
urlpatterns = [
    path('', include(router.urls)),
    re_path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
