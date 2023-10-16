from django.contrib import admin


from servicos.models import TiposServicos, SolicitacaoServico

# Register your models here.
admin.site.register(TiposServicos)
admin.site.register(SolicitacaoServico)
