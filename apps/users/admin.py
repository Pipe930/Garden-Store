from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['username', 'email']

admin.site.register(User, UserAdmin)