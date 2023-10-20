from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from django.contrib.auth.models import User

from django.contrib.auth.models import Group
from acessos.models import CustomUser

from django.contrib.messages import constants
from django.contrib import messages


from django.contrib.auth.decorators import login_required
from .decorators import gerente_required, atendente_required

from servicos.models import SolicitacaoServico, TiposServicos
# Create your views here.
from .forms import AtendenteForm


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


@login_required
@gerente_required
def lista_atendentes(request):
    # pega o grupo de atendentes
    # group = Group.objects.get(name='atendentes')
    # Obtenha todos os usuários que pertencem ao grupo 'atendentes' e ordene-os por nome
    # atendentes = User.objects.filter(groups=group).order_by('username')
    atendentes = CustomUser.objects.filter(
        groups__name='atendentes').order_by('nome')
    return render(request, 'lista_atendentes.html', {'atendentes': atendentes})


@login_required
@gerente_required
def detalhe_atendente(request, atendente_id):
    atendente = get_object_or_404(CustomUser, pk=atendente_id)

    if atendente.groups.filter(name='atendentes').exists():
        return render(request, 'detalhe_atendente.html', {'atendente': atendente})
    else:
        return HttpResponseForbidden("Acesso não autorizado")


@login_required
@gerente_required
def cadastra_atendente(request):
    if request.method == 'POST':
        form = AtendenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista-atendentes')
    else:
        form = AtendenteForm()
    return render(request, 'cadastra_atendente.html', {'form': form})


@login_required
@gerente_required
def edita_atendente(request, atendente_id):
    atendente = get_object_or_404(CustomUser, pk=atendente_id)

    if not atendente.groups.filter(name='atendentes').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        form = AtendenteForm(request.POST, instance=atendente)
        if form.is_valid():
            form.save()
            return redirect('lista-atendentes')
    else:
        form = AtendenteForm(instance=atendente)
    return render(request, 'edita_atendente.html', {'form': form})


@login_required
@gerente_required
def inativa_atendente(request, atendente_id):
    atendente = get_object_or_404(CustomUser, pk=atendente_id)

    if not atendente.groups.filter(name='atendentes').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        atendente.is_active = False
        atendente.save()
        return redirect('lista-atendentes')
    return render(request, 'inativa_atendente.html', {'atendente': atendente})


@login_required
@gerente_required
def ativa_atendente(request, atendente_id):
    atendente = get_object_or_404(CustomUser, pk=atendente_id)

    if not atendente.groups.filter(name='atendentes').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        atendente.is_active = True
        atendente.save()
        return redirect('lista-atendentes')
    return render(request, 'ativa_atendente.html', {'atendente': atendente})
