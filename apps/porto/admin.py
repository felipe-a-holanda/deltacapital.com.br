from django.contrib import admin

from .models import PropostaPorto


@admin.action(description="Enviar propostas selecionadas por email")
def send_email(modeladmin, request, queryset):
    for p in queryset:
        p.send_mail()


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
    actions = [send_email]

    readonly_fields = ["session_hash", "pagina"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_operador:
            return qs.filter(user=request.user)
        return qs
