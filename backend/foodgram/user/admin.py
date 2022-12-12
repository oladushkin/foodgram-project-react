from django.contrib import admin

from .models import Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('email', 'username')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


admin.site.register(Follow, FollowAdmin)
