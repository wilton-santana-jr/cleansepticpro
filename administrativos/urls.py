from django.urls import path
from . import views

urlpatterns = [
    path('atendimentos/', views.atendimentos, name="atendimentos"),
    path('relatorios/', views.relatorios, name="relatorios"),

    path('atendentes/', views.lista_atendentes, name='lista-atendentes'),
    path('atendentes/<int:atendente_id>/',
         views.detalhe_atendente, name='detalhe-atendente'),
    path('atendentes/novo/', views.cadastra_funcionario, name='cadastra-funcionario'),
    path('atendentes/<int:atendente_id>/edita/',
         views.edita_atendente, name='edita-atendente'),
    path('atendentes/<int:atendente_id>/inativa/',
         views.inativa_atendente, name='inativa-atendente'),
    path('atendentes/<int:atendente_id>/ativa/',
         views.ativa_atendente, name='ativa-atendente'),

     path('helpers/', views.lista_helpers, name='lista-helpers'),
     path('helpers/<int:helper_id>/edita/',
         views.edita_helper, name='edita-helper'),
         path('helpers/<int:helper_id>/inativa/',
         views.inativa_helper, name='inativa-helper'),
    path('helpers/<int:helper_id>/ativa/',
         views.ativa_helper, name='ativa-helper'),

    path('servicos/', views.lista_servicos, name='lista-servicos'),
    path('servicos/<int:servico_id>/',
         views.detalhe_servico, name='detalhe-servico'),
    path('servicos/novo/', views.cadastra_servico, name='cadastra-servico'),
    path('servicos/<int:servico_id>/edita/',
         views.edita_servico, name='edita-servico'),
    path('servicos/<int:servico_id>/inativa/',
         views.inativa_servico, name='inativa-servico'),
    path('servicos/<int:servico_id>/ativa/',
         views.ativa_servico, name='ativa-servico'),    
         

]
