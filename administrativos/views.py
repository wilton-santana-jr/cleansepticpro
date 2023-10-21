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
from .forms import FuncionarioForm, ServicoForm


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


##################################################################
# GERÊNCIA DE ATENDENTES PELO GERENTE
##################################################################

@login_required
@gerente_required
def lista_atendentes(request):
    # Obtenha todos os usuários que pertencem ao grupo 'atendentes' e ordene-os por nome
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
def cadastra_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, constants.SUCCESS,
                                 'Funcionário {nome_funcionario} salvo com sucesso'.format(nome_funcionario = form.cleaned_data['nome']))
            return redirect('lista-atendentes')
    else:
        form = FuncionarioForm()
    return render(request, 'cadastra_atendente.html', {'form': form})


@login_required
@gerente_required
def edita_atendente(request, atendente_id):
    atendente = get_object_or_404(CustomUser, pk=atendente_id)

    if not atendente.groups.filter(name='atendentes').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=atendente)
        if form.is_valid():
            form.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Atendente {} editado com sucesso'.format(atendente.nome))
            return redirect('lista-atendentes')
    else:
        form = FuncionarioForm(instance=atendente)
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

        messages.add_message(request, constants.SUCCESS,
                                 'Atendente {} inativado com sucesso'.format(atendente.nome))
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

        messages.add_message(request, constants.SUCCESS,
                                 'Atendente {} ativado com sucesso'.format(atendente.nome))
        return redirect('lista-atendentes')
    return render(request, 'ativa_atendente.html', {'atendente': atendente})


##################################################################
# GERÊNCIA DE SERVIÇOS DE LIMPEZA PELO GERENTE
##################################################################


@login_required
@gerente_required
def lista_servicos(request):
    # Obtenha todos os usuários que pertencem ao grupo 'atendentes' e ordene-os por nome
    servicos = TiposServicos.objects.all()
    return render(request, 'lista_servicos.html', {'servicos': servicos})


@login_required
@gerente_required
def detalhe_servico(request, servico_id):
    servico = get_object_or_404(TiposServicos, pk=servico_id)
    return render(request, 'detalhe_servico.html', {'servico': servico})


@login_required
@gerente_required
def cadastra_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Novo serviço cadastrado')
            return redirect('lista-servicos')
    else:
        form = ServicoForm()
    return render(request, 'cadastra_servico.html', {'form': form})


@login_required
@gerente_required
def edita_servico(request, servico_id):
    servico = get_object_or_404(TiposServicos, pk=servico_id)
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Serviço {} editado com sucesso'.format(servico.nome))
            return redirect('lista-servicos')
    else:
        form = ServicoForm(instance=servico)
    return render(request, 'edita_servico.html', {'form': form})


@login_required
@gerente_required
def inativa_servico(request, servico_id):
    servico = get_object_or_404(TiposServicos, pk=servico_id)
    if request.method == 'POST':
        servico.disponivel = False
        servico.save()

        messages.add_message(request, constants.SUCCESS,
                                 'Serviço {} inativado com sucesso'.format(servico.nome))
        return redirect('lista-servicos')
    return render(request, 'inativa_servico.html', {'servico': servico})


@login_required
@gerente_required
def ativa_servico(request, servico_id):
    servico = get_object_or_404(TiposServicos, pk=servico_id)

    if request.method == 'POST':
        servico.disponivel = True
        servico.save()

        messages.add_message(request, constants.SUCCESS,
                                 'Serviço {} ativado com sucesso'.format(servico.nome))
        return redirect('lista-servicos')
    return render(request, 'ativa_servico.html', {'servico': servico})


##################################################################
# GERÊNCIA DE SOLICITAÇÕES DE SERVIÇOS DE LIMPEZA SOLICITADOS PELOS CLIENTES.
# QUEM GERENCIA ESSAS SOLICITAÇÕES SÃO OS ATENDENTES
##################################################################

##################################################################
# GERÊNCIA DE HELPERS PELO GERENTE
##################################################################

@login_required
@gerente_required
def lista_helpers(request):
    # Obtenha todos os usuários que pertencem ao grupo 'helpers' e ordene-os por nome
    helpers = CustomUser.objects.filter(
        groups__name='helpers').order_by('nome')
    return render(request, 'lista_helpers.html', {'helpers': helpers})


@login_required
@gerente_required
def edita_helper(request, helper_id):
    helper = get_object_or_404(CustomUser, pk=helper_id)

    if not helper.groups.filter(name='helpers').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=helper)
        if form.is_valid():
            form.save()

            messages.add_message(request, constants.SUCCESS,
                                 'Helper {} editado com sucesso'.format(helper.nome))
            return redirect('lista-helpers')
    else:
        form = FuncionarioForm(instance=helper)
    return render(request, 'edita_helper.html', {'form': form})


@login_required
@gerente_required
def inativa_helper(request, helper_id):
    helper = get_object_or_404(CustomUser, pk=helper_id)

    if not helper.groups.filter(name='helpers').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        helper.is_active = False
        helper.save()

        messages.add_message(request, constants.SUCCESS,
                                 'Helper {} inativado com sucesso'.format(helper.nome))
        return redirect('lista-helpers')
    return render(request, 'inativa_helper.html', {'helper': helper})


@login_required
@gerente_required
def ativa_helper(request, helper_id):
    helper = get_object_or_404(CustomUser, pk=helper_id)

    if not helper.groups.filter(name='helpers').exists():
        return HttpResponseForbidden("Acesso não autorizado")

    if request.method == 'POST':
        helper.is_active = True
        helper.save()

        messages.add_message(request, constants.SUCCESS,
                                 'Helper {} ativado com sucesso'.format(helper.nome))
        return redirect('lista-helpers')
    return render(request, 'ativa_helper.html', {'helper': helper})