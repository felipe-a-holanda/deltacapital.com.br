from django.contrib import admin

from .models import PropostaPorto


@admin.register(PropostaPorto)
class PropostaAdmin(admin.ModelAdmin):
    list_display = [
        "criado_em",
        "user",
        "nome",
        "cpf",
        "valor_do_veiculo",
        "enviado_em",
    ]

    readonly_fields = ["session_hash", "stage"]
