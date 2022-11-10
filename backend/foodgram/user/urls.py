from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter
from .views import APIFollowList

router = SimpleRouter()
router.register(
    'follow',
    APIFollowList
)
urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
