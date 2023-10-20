from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from acessos.models import CustomUser


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'nome', 'telefone', 'endereco')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nome', 'telefone', 'endereco')}),
    )
    form = CustomUserChangeForm


admin.site.register(CustomUser, CustomUserAdmin)
