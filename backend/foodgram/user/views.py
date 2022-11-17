from rest_framework import filters, mixins, viewsets
from .serializers import CustomUserSerializer, FollowSerializer
from .models import User, Follow
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet
from rest_framework.pagination import LimitOffsetPagination


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class APIFollowList(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()
