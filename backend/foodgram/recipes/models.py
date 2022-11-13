from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class Tag(models.Model):
    """Тег рецептов."""
    name = models.CharField(
        max_length=50,
        help_text='Название тега.'
    )
    сolor = ColorField(default='#FF0000')
    slug = models.SlugField(max_length=50,)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингридиенты"""
    name = models.CharField(max_length=100,)
    measurement_unit = models.CharField(max_length=20,)

    def __str__(self):
        return self.name


class Array(models.Model):
    """Список ингридиентов в рецепте"""
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )
    amount = models.IntegerField()


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through=Array,
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
        verbose_name='Тег рецепта'
    )
    image = models.ImageField(
        upload_to='recipe/images/',
        null=True,
        default=None
        )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
    )
    text = models.CharField(
        max_length=200,
        verbose_name='Орисание',
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(1),
        ),
        verbose_name='Время приготавления',
        help_text='В минутах',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )


class TagsRecipes(models.Model):
    """Теги для рецепта"""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    recipes = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
