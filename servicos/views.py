from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.models import Group
from acessos.models import CustomUser

from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from servicos.decorators import cliente_required, gerente_required, atendente_required

from .models import SolicitacaoServico, TiposServicos


@login_required  # Requer que o usuário esteja autenticado
@cliente_required
def listagem(request):
    if request.method == "GET":

        solicitacoes_servicos = SolicitacaoServico.objects.filter(cliente=request.user)
        return render(request, 'listagem.html', {'servicos': solicitacoes_servicos})
    
    
@login_required
@cliente_required
def cadastro_servico(request):
    if request.method == "GET":
        return render(request, 'cadastro-servico.html')
    else:
        tipo_servico = request.POST.get('tipo_servico')
        data_limpeza = request.POST.get('data_limpeza')
        endereco = request.POST.get('endereco')

        if not tipo_servico:
            messages.add_message(request, constants.ERROR,
                                 'Selecione o tipo do serviço')
            return redirect('/servicos/cadastro-servico')
        
        if tipo_servico == 'limpeza_simples':
            tipo_servico = 'S'
        if tipo_servico == 'limpeza_profunda':
            tipo_servico = 'P'

        servico = TiposServicos.objects.get(tipo=tipo_servico)

        
        if not data_limpeza:
            messages.add_message(request, constants.ERROR,
                                 'Selecione data e hora da limpeza')
            return redirect('/servicos/cadastro-servico')
        
        if not endereco:
            messages.add_message(request, constants.ERROR,
                                 'Selecione o endereço onde será realizado o serviço')
            return redirect('/servicos/cadastro-servico')
        
        print(tipo_servico)
        print(data_limpeza)
        print(endereco)


        try:
            solicitacao_servico = SolicitacaoServico.objects.create(
                servico=servico,
                data_limpeza=data_limpeza,
                cliente=request.user,
                status='S',
            )

            messages.add_message(request, constants.SUCCESS,
                                 'Solicitação de serviço salva com sucesso')
        except:
            messages.add_message(
                request, constants.ERROR, 'Erro interno do sistema, contate um administrador')
            return redirect('/servicos/cadastro-servico')

        return redirect('/servicos/listagem/')


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
