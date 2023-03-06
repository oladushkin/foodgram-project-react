from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Follow, User
from .paginator import FollowPaginator
from .serializers import BriefUser, CustomUserSerializer, FollowSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def follow_list(request):
    """Вывод подписок"""
    paginator = FollowPaginator()
    user = request.user
    followers = Follow.objects.filter(user=user)
    foll_prof = []
    for follower in followers:
        foll_prof.append(follower.following)
    result_page = paginator.paginate_queryset(foll_prof, request)
    serializer = BriefUser(
        result_page,
        many=True,
        context={'request': request}
    )
    the_data = serializer.data
    return paginator.get_paginated_response(the_data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_follow(request, user_id):
    """Создание и удаление подписок"""
    following = get_object_or_404(User, pk=user_id)
    user = request.user
    data_follow = {'following': user_id, 'user': user.id}
    if request.method == 'POST':
        serializer = FollowSerializer(data=data_follow)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    follow = Follow.objects.filter(user=request.user, following=following)
    follow.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
