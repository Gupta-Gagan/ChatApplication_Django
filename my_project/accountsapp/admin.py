from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_online')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {
            'fields': ('phone', 'bio', 'profile_picture', 'is_online', 'last_seen'),
        }),
    )
