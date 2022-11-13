from rest_framework import filters, mixins, viewsets, status
from .serializers import CustomUserSerializer, FollowSerializer, RegistrationSerializer
from .models import User, Follow
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)

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


@api_view(['POST'])
def user_registration(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        user.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)