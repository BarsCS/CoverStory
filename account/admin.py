from django.contrib import admin

from .models import Profile, Follow

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display_links = []
    list_display = [
        'user',
        'avatar',
        'name',
        'created',
        'description',
    ]
    ordering = ['-created', 'name']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display_links = []
    list_display = [
        'user_from',
        'user_to'
    ]
