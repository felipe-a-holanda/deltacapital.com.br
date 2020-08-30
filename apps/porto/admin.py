from django.contrib import admin

from .models import PropostaPorto


@admin.register(PropostaPorto)
class PropostaAdmin(admin.ModelAdmin):
    list_display = [
        "criado_em",
        "status",
        "user",
        "nome",
        "cpf",
        "valor_do_veiculo",
        "enviado_em",
    ]

    list_filter = ["status"]

    def estado(self, obj):
        return obj.get_status_display()

    readonly_fields = ["session_hash", "stage"]
