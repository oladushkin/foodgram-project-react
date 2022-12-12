from recipes.models import Ingredient, Tag
from rest_framework import serializers


def validate_ingredient(ingredients):
    if len(ingredients) < 1:
        raise serializers.ValidationError(
            'Поле ингредиента обязательно.'
        )
    for ingredient in ingredients:
        try:
            Ingredient.objects.get(id=ingredient['id'])
        except serializers.ValidationError:
            raise serializers.ValidationError(
                f'NO {ingredient}'
            )


def validate_tags(tags):
    if len(tags) <= 0:
        raise serializers.ValidationError(
            'Пеле тега обязательно.'
        )
    for tag in tags:
        try:
            Tag.objects.get(id=tag)
        except serializers.ValidationError:
            raise serializers.ValidationError(
                f'Такого тега нет: {tag}'
            )
