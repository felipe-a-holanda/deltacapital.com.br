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

    readonly_fields = ["session_hash", "stage"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_operador:
            return qs.filter(user=request.user)
        return qs
