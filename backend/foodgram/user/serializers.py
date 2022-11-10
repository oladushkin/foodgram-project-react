from djoser.serializers import UserSerializer
from rest_framework import serializers
from user.models import User, Follow
from rest_framework.validators import UniqueTogetherValidator

class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписчиков"""
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
        slug_field='username',
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            ),
        ]
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data