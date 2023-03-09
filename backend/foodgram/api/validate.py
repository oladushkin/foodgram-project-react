from recipes.models import Ingredient, Tag
from rest_framework import serializers


def validate_ingredient(ingredients):
    list_id_ingredient = []
    if len(ingredients) <= 0:
        raise serializers.ValidationError(
            'Поле ингредиента обязательно.'
        )
    for ingredient in ingredients:
        list_id_ingredient.append(ingredient['id'])
        try:
            Ingredient.objects.get(id=ingredient['id'])
        except serializers.ValidationError:
            raise serializers.ValidationError(
                f'NO {ingredient}'
            )
    for id_ingredient in list_id_ingredient:
        if list_id_ingredient.count(id_ingredient) > 1:
            raise serializers.ValidationError(
                (f'Два одинаковых ингредиента запрещены: '
                 f'{Ingredient.objects.get(id=id_ingredient).name}')
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
