from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        )
    color = models.CharField(
        max_length=50,
    )
    slug = models.SlugField(
        max_lenght=50,
        )


class Ingredient(models.Model):
    name = models.CharField(
        max_lenght=100,
    )
    measurement_unit = models.CharField(
        max_length=20,
    )


class Array(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    amount = models.IntegerField()


class Recipe(models.Model):
    ingredient = models.ForeignKey(
        Array,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes'
    )
    image = models.ImageField(
        upload_to='recipe/images/', 
        null=True,  
        default=None
        )
