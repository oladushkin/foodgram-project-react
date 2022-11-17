from rest_framework import serializers
from user.models import User
from recipes.models import Recipe, Ingredient, Tag, Array, TagsRecipes, Favorite, ShoppingList
from drf_extra_fields.fields import Base64ImageField


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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""
    ingredients = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    image = Base64ImageField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'author', 'ingredients', 'tags',
            'image', 'name', 'text',
            'cooking_time', 'is_in_shopping_cart', 'is_favorited',
        )
        read_only_fields = ('author',)
    
    def get_ingredients(self, recipe):
        ingredients = []
        for ingredient in recipe.ingredients.all():
            ingredients.append(
                {
                    'id': ingredient.pk,
                    'amount': ingredient.ingredient_recipe.get(
                        recipe=recipe).amount,
                    'name': ingredient.name,
                    'measurement_unit': ingredient.measurement_unit
                }
            )
        return ingredients
    def to_internal_value(self, data):
            new_data = super().to_internal_value(data)
            new_data['ingredients'] = data['ingredients']
            new_data['tags'] = data['tags']
            return new_data

    def create(self, validated_data):
        print(validated_data)
        ingrediens = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingrediens:
            Array.objects.create(
                ingredient=ingredient.id,
                recipe=recipe,
                amount=ingredient.amount
            )
        for tag in tags:
            TagsRecipes.objects.create(
                tag=tag, recipe=recipe
            )       
        return recipe

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


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = Favorite
        fields = ('recipe')


class ShoppingSerializer(serializers.ModelSerializer):
    recipe = serializers.SlugRelatedField(
        queryset=Recipe.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = ShoppingList
        fields = ('recipe')
