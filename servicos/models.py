from django.db import models


from django.contrib.auth.models import User
from acessos.models import CustomUser

from django.utils.safestring import mark_safe
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta


# Create your models here.

class TiposServicos(models.Model):

    nome = models.CharField(max_length=50)

    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    def preco_formatado(self):
        return f'R$ {self.preco:.2f}'

    def desc(self):
        return f'{self.nome} (R$ {self.preco:.2f})'


class SolicitacaoServico(models.Model):
    choice_status = (
        ('S', 'Solicitado'),
        ('P', 'Pendente'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )

    choice_forma_pagamento = (
        ('D', 'Dinheiro em Espécie'),
        ('P', 'PIX'),
        ('C', 'Cartão de Crédito'),
    )

    cliente = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='solicitacoes_cliente')
    atendente = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                  null=True, blank=True, related_name='solicitacoes_atendente')
    servico = models.ForeignKey(TiposServicos, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    forma_pagamento = models.CharField(
        max_length=2, choices=choice_forma_pagamento, null=True, blank=True)
    dar_desconto = models.BooleanField(default=False, blank=True)
    valor_desconto = models.FloatField(null=True, blank=True)
    valor_pago = models.FloatField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    data_limpeza = models.DateTimeField(null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.cliente} | {self.servico.nome} | {self.criado_em.strftime("%d/%m/%Y %Hh:%M:%S")}'

    def save(self, *args, **kwargs):
        if self.dar_desconto:
            self.valor_pago = self.servico.preco - self.valor_desconto
        else:
            self.valor_pago = self.servico.preco
        super().save(*args, **kwargs)

    def valor_pago_formatado(self):
        return f'R$ {self.valor_pago:.2f}'

    def valor_desconto_formatado(self):
        return f'R$ {self.valor_desconto:.2f}'

    def badge_template(self):
        status_mapping = {
            'S': ('bg-info text-white', 'Solicitado'),
            'P': ('bg-warning text-dark', 'Pendente'),
            'R': ('bg-success', 'Realizado'),
            'C': ('bg-danger text-white', 'Cancelado')
        }

        classes_css, texto = status_mapping.get(
            self.status, ('bg-secondary', 'Desconhecido'))
        return mark_safe(f"<span class='badge {classes_css}'>{texto}</span>")
