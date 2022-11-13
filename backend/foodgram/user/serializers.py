from rest_framework import serializers
from user.models import User, Follow
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        extra_kwargs = {'password': {'write_only': True}}


    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


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