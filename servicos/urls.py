from django.urls import path
from . import views

urlpatterns = [
    path('listagem/', views.listagem, name="listagem"),
    path('atendimentos/', views.atendimentos, name="atendimentos"),
    path('relatorios/', views.relatorios, name="relatorios"),
    path('cadastro-servico', views.cadastro_servico, name='cadastro-servico'),
]
