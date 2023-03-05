from drf_extra_fields.fields import Base64ImageField
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
            'id', 'name', 'measurement_unit'
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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.BooleanField(
        read_only=True,
        default=False
    )
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True,
        default=False
    )

    class Meta:
        model = Recipe
        fields = '__all__'

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


class POST_RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
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

    @staticmethod
    def _add_ingredients_and_tags(recipe, ingredients, tags):
        recipe.tags.set(tags)
        ingredients_list = []
        for i in ingredients:
            ingredient = Ingredient.objects.get(id=i.get('id'))
            amount = i.get('amount')
            ingredient_recipe, _ = Ingredients_Recipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            ingredients_list.append(ingredient_recipe)
        return recipe

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        return self._add_ingredients_and_tags(
            recipe,
            ingredients,
            tags
        )

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe.ingredients.clear()
        recipe.tags.clear()
        super().update(validated_data=validated_data, instance=recipe)
        recipe.save()
        return self._add_ingredients_and_tags(
            recipe,
            ingredients,
            tags
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        validate_ingredient(ingredients)
        validate_tags(tags)
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data


class BRIEF_RECIPE(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных рецептов"""
    recipe = BRIEF_RECIPE(
        read_only=True
    )

    class Meta:
        model = Favorite
        fields = ('recipe',)


class ShoppingSerializer(serializers.ModelSerializer):
    recipe = BRIEF_RECIPE(
        read_only=True
    )

    class Meta:
        model = ShoppingList
        fields = ('recipe',)
