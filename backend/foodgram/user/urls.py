from django.urls import include, path, re_path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, api_follow, follow_list

app_name = 'users'

router = SimpleRouter()
router.register(
    'users',
    UserViewSet
)
urlpatterns = [
    path('users/subscriptions/', follow_list),
    path('users/<int:user_id>/subscribe/', api_follow),
    path('', include(router.urls)),
    re_path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
