from django.contrib import admin

from .models import Proposta


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ["criado_em", "nome", "cpf", "valor_do_veiculo", "enviado_em"]

    readonly_fields = ["session_hash", "stage"]
