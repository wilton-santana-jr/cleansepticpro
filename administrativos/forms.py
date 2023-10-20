from django import forms
from django.contrib.auth.models import Group
from acessos.models import CustomUser
from servicos.models import TiposServicos
from django import forms


class AtendenteForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password',
                  'nome', 'telefone', 'endereco']
        labels = {
            'username': 'Login',
            'password': 'Senha',
            'email': 'E-mail',
            'nome': 'Nome',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            # Adicione mais campos e rótulos aqui
        }
        widgets = {
            # Defina o número de linhas desejado, por exemplo, 3
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input-default w100'})

    def save(self, commit=True):
        # Chame o método save do modelo para criar o usuário
        instance = super(AtendenteForm, self).save(commit=False)

        if commit:
            # Primeiro, salve o objeto para obter um ID
            instance.save()

        # Certifique-se de que o usuário seja adicionado ao grupo "atendentes"
        atendentes_group, created = Group.objects.get_or_create(
            name='atendentes')
        instance.groups.add(atendentes_group)

        if commit:
            instance.save()

        return instance

    def clean_password(self):
        # Use a função set_password() para definir a senha criptografada
        password = self.cleaned_data.get('password')
        if password:
            self.instance.set_password(password)
        return password

    def clean(self):
        # Certifique-se de que a senha seja atualizada apenas se um novo valor de senha for fornecido
        cleaned_data = super(AtendenteForm, self).clean()
        if not cleaned_data.get('password'):
            self.instance.set_unusable_password()
        return cleaned_data


class ServicoForm(forms.ModelForm):

    # TIPO_CHOICES = (
    #    ('P', 'Limpeza Profunda'),
    #    ('S', 'Limpeza Simples'),
    # )

    # tipo = forms.ChoiceField(choices=TIPO_CHOICES, required=True, widget=forms.Select(attrs={'class': 'input-default w100'}))

    class Meta:
        model = TiposServicos
        fields = ['nome', 'preco',
                  'disponivel']
        labels = {
            'nome': 'Nome do Tipo de Limpeza',
            'preco': 'Preço (R$)',
            'disponivel': 'Disponível',
            # Adicione mais campos e rótulos aqui
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['tipo'].empty_label = None

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'input-default w100'})

    def save(self, commit=True):
        # Chame o método save do modelo para criar o servico
        instance = super(ServicoForm, self).save(commit=False)

        if commit:
            # Primeiro, salve o objeto para obter um ID
            instance.save()

        return instance
