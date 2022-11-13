from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('email', 'username')
