from django.urls import path
from . import views

urlpatterns = [
    path('listagem/', views.listagem, name="listagem"),
    path('cadastro-servico', views.cadastro_servico, name='cadastro-servico'),
]
