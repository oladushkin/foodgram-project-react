from djoser.serializers import UserSerializer
from rest_framework import serializers
from user.models import User
from recipes.models import Recipe, Ingredient, Tag, Array, TagsRecipes, Favorite
import base64
from django.core.files.base import ContentFile

class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов"""
    class Meta:
        model = Ingredient
        fields = (
            'name', 'measurement_unit',
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = (
            'name', 'color', 'slag',
        )


class Base64ImageField(serializers.ImageField):
    """Кодировка изображений"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""
    ingredient = IngredientSerializer(read_only=True, many=True)
    author = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'author', 'ingredient', 'tags',
            'image', 'name', 'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingrediens = validated_data.pop('ingredient')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingrediens:
            current_ingredien, status = Ingredient.objects.get_or_create(
                **ingredient)
            Array.objects.create(
                ingredient=current_ingredien, recipe=recipe
            )
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(
                **tag
            )
            TagsRecipes.objects.create(
                tag=current_tag, recipe=recipe
            )
        
        return recipe


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Favorite
        fields = ('recipe')