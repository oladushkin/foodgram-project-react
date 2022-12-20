import base64

from django.core.files.base import ContentFile
from recipes.models import (Favorite, Ingredient, Ingredients_Recipe, Recipe,
                            ShoppingList, Tag, TagsRecipes)
from rest_framework import serializers
from user.serializers import CustomUserSerializer

from .validate import validate_ingredient, validate_tags


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов"""
    class Meta:
        model = Ingredient
        fields = (
            'name', 'measurement_unit'
        )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


class TagsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        slug_field='id',
        source='tag'
    )

    class Meta:
        model = TagsRecipes
        fields = ('id',)


class Ingredients_RecipeSerializer(serializers.ModelSerializer):
    id = serializers.SlugRelatedField(
        queryset=Ingredient.objects.all(),
        slug_field='id',
        source='ingredient'
    )

    class Meta:
        model = Ingredients_Recipe
        fields = ('id', 'amount')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags',
            'image', 'name', 'text',
            'cooking_time', 'is_in_shopping_cart', 'is_favorited',
        )

    def get_ingredients(self, recipe):
        ingredients = []
        for ingredient in recipe.ingredients.all():
            ingredients.append(
                {
                    'id': ingredient.pk,
                    'amount': ingredient.ingredients_recipe.get(
                        recipe=recipe).amount,
                    'name': ingredient.name,
                    'measurement_unit': ingredient.measurement_unit
                }
            )
        return ingredients

    def _get_user(self):
        return self.context['request'].user

    def get_is_favorited(self, request):
        user = self._get_user()
        if user.is_authenticated:
            return request.favorite_recipe.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, request):
        user = self._get_user()
        if user.is_authenticated:
            return request.shopping_recipe.filter(user=user).exists()
        return False


class POST_RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = Ingredients_RecipeSerializer(many=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags',
            'image', 'name', 'text',
            'cooking_time'
        )

    def _get_user(self):
        return self.context['request'].user

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self._get_user()
        recipe = Recipe.objects.create(author=user, **validated_data)
        for ingredient in ingredients:
            print(*ingredient)
            Ingredients_Recipe.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )
        for tag in tags:
            TagsRecipes.objects.create(
                tag=Tag.objects.get(id=tag),
                recipes=recipe
            )
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time',
            recipe.cooking_time
        )
        recipe.save
        for ingredient in ingredients:
            Ingredients_Recipe.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            )
        for tag in tags:
            TagsRecipes.objects.create(
                tag=Tag.objects.get(id=tag),
                recipes=recipe
            )
        return recipe

    def to_representation(self, recipe):
        ingredients_recipe = recipe.ingredients_recipe.all()
        representation = super().to_representation(recipe)
        print(representation)
        representation['ingredients'] = []
        for ingredient in ingredients_recipe:
            representation['ingredients'].append(ingredient.ingredient)
        return representation

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        tags = self.initial_data['tags']
        validate_ingredient(ingredients)
        validate_tags(tags)
        data = self.initial_data
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    recipe = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class ShoppingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    recipe = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = ShoppingList
        fields = ('user', 'recipe')
