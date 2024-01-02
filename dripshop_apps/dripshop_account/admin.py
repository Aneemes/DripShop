# dripshop_apps/dripshop_account/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'address', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(UserAccount, CustomUserAdmin)
