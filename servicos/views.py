from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.models import Group
from acessos.models import CustomUser

from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from servicos.decorators import cliente_required, gerente_required, atendente_required


@login_required  # Requer que o usuário esteja autenticado
@cliente_required
def listagem(request):
    if request.method == "GET":
        return render(request, 'listagem.html')


@login_required
@gerente_required
def relatorios(request):
    if request.method == "GET":
        return render(request, 'relatorios.html')


@login_required
@atendente_required
def atendimentos(request):
    if request.method == "GET":
        return render(request, 'atendimentos.html')
