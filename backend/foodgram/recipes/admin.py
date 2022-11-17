from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Array, TagsRecipes, Favorite, ShoppingList


class ArrayInline(admin.StackedInline):
    model = Array
    extra = 1


class TagInLine(admin.StackedInline):
    model = TagsRecipes
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'count_in_favorite')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'
    inlines = [ArrayInline, TagInLine]

    def count_in_favorite(self, obj):
        from django.db.models import Count
        result = Favorite.objects.filter(recipe=obj).aggregate(Count('recipe'))
        return result['recipe__count']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(ShoppingList)