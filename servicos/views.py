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

        solicitacoes_servicos = SolicitacaoServico.objects.filter(
            cliente=request.user).order_by('-criado_em')
        return render(request, 'listagem.html', {'servicos': solicitacoes_servicos})


@login_required
@cliente_required
def cadastro_servico(request):
    if request.method == "GET":

        tipos_servicos = TiposServicos.objects.all()
        choice_forma_pagamento = SolicitacaoServico.choice_forma_pagamento
        # faltou passar o tipo de servico aqui para carregar o select dinamicamente
        return render(request, 'cadastro-servico.html', {'tipos_servicos': tipos_servicos,
                                                         'choice_forma_pagamento': choice_forma_pagamento})
    else:

        data_limpeza = request.POST.get('data_limpeza')
        # tipo_servico_id = request.POST.getlist('servicos') # retorna uma lista de ids quando o select é multiple
        # retorna somente um id quando o select não é multiple
        tipo_servico_id = request.POST.get('servicos')
        endereco = request.POST.get('endereco')
        forma_pagamento = request.POST.get('forma_pagamento')

        if not tipo_servico_id:
            messages.add_message(request, constants.ERROR,
                                 'Selecione o tipo do serviço')
            return redirect('/servicos/cadastro-servico')

        tipo_servico = TiposServicos.objects.get(
            id=tipo_servico_id)  # para um id
        # tipo_servico = TiposServicos.objects.filter(id__in=tipo_servico_id) #para multiplos ids

        if not data_limpeza:
            messages.add_message(request, constants.ERROR,
                                 'Selecione data e hora da limpeza')
            return redirect('/servicos/cadastro-servico')

        if not endereco:
            messages.add_message(request, constants.ERROR,
                                 'Selecione o endereço onde será realizado o serviço')
            return redirect('/servicos/cadastro-servico')

        if forma_pagamento not in [choice[0] for choice in SolicitacaoServico.choice_forma_pagamento]:
            messages.add_message(request, constants.ERROR,
                                 'Forma de pagamento inválida')
            return redirect('/servicos/cadastro-servico')

        try:
            solicitacao_servico = SolicitacaoServico.objects.create(
                servico=tipo_servico,
                data_limpeza=data_limpeza,
                cliente=request.user,
                forma_pagamento=forma_pagamento,
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
