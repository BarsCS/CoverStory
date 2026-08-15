from django.contrib import admin

from .models import Profile

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
