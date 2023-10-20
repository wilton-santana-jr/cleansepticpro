# forms.py

from django import forms
from django.contrib.auth.models import Group
from acessos.models import CustomUser


class AtendenteForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        # Chame o método save do modelo para criar o usuário
        instance = super(AtendenteForm, self).save(commit=False)

        # Certifica-se de que o usuário seja adicionado ao grupo "atendentes"
        atendentes_group, created = Group.objects.get_or_create(
            name='atendentes')
        instance.groups.add(atendentes_group)

        if commit:
            instance.save()

        return instance
