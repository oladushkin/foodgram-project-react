from django.db import models
from django.core.validators import MinValueValidator
from user.models import User


class Tag(models.Model):
    """Тег рецептов."""
    name = models.CharField(
        max_length=50,
        )
    color = models.CharField(
        max_length=50,
    )
    slug = models.SlugField(
        max_length=50,
        )


class Ingredient(models.Model):
    """Ингридиенты"""
    name = models.CharField(
        max_length=100,
    )
    measurement_unit = models.CharField(
        max_length=20,
    )


class Array(models.Model):
    """Список ингридиентов в рецепте"""
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    amount = models.IntegerField()


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through=Array,
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
    )
    image = models.ImageField(
        upload_to='recipe/images/', 
        null=True,  
        default=None
        )
    name = models.CharField(
        max_length=200,
    )
    text = models.CharField(
        max_length=200,
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(1),
        ),
        verbose_name='Время приготавления',
        help_text='Указывать время в минутах',
    )


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )