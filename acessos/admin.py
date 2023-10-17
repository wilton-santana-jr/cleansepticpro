from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from acessos.models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(CustomUser, CustomUserAdmin)