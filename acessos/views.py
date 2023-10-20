from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.models import Group
from acessos.models import CustomUser

from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not nome:
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu nome completo com nome e sobrenome')
            return redirect('/acessos/cadastro')

        nome_dividido = nome.split()

        if not (len(nome_dividido) >= 2):
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu nome completo com nome e sobrenome')
            return redirect('/acessos/cadastro')

        first_name = nome_dividido[0]
        last_name = " ".join(nome_dividido[1:])

        if not telefone:
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu telefone')
            return redirect('/acessos/cadastro')

        if not endereco:
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu endereço')
            return redirect('/acessos/cadastro')

        if not username:
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu username sem espaços')
            return redirect('/acessos/cadastro')

        if not email:
            messages.add_message(request, constants.ERROR,
                                 'Preencha seu email')
            return redirect('/acessos/cadastro')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'As senhas não coincidem')
            return redirect('/acessos/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'Sua senha deve ter 7 ou mais dígitos')
            return redirect('/acessos/cadastro')

        try:
            user = CustomUser.objects.create_user(
                nome=nome,
                first_name=first_name,
                last_name=last_name,
                telefone=telefone,
                endereco=endereco,
                username=username,
                email=email,
                password=senha,
            )

            # Verifique se o grupo 'clientes' existe
            grupo_clientes, created = Group.objects.get_or_create(
                name='clientes')
            # Associe o usuário ao grupo 'clientes'
            user.groups.add(grupo_clientes)

            messages.add_message(request, constants.SUCCESS,
                                 'Usuário salvo com sucesso')
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema, contate um administrador')
            return redirect('/acessos/cadastro')

        return redirect('/acessos/login/')


def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
    if user:
        login(request, user)

        if user.groups.filter(name='clientes').exists():
            # view de listagem de serviços
            return redirect('/servicos/listagem')
        elif user.groups.filter(name='atendentes').exists():
            return redirect('/administrativos/atendimentos')
        elif user.groups.filter(name='gerentes').exists():
            return redirect('/administrativos/relatorios')
        else:
            return redirect('/acessos/login')

    else:
        messages.add_message(request, constants.ERROR,
                             'Usuário ou senha inválidos')
        return redirect('/acessos/login')
