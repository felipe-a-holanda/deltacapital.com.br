from django.contrib import admin

from .models import CapitalGiro
from .models import CartaoCredito
from .models import FinanciamentoVeiculo


@admin.register(FinanciamentoVeiculo)
class FinanciamentoVeiculoAdmin(admin.ModelAdmin):
    list_display = ["cpf", "telefone", "email", "tipo_veiculo", "valor_do_veiculo", "criado_em"]
    list_filter = ["tipo_veiculo", "criado_em"]


@admin.register(CartaoCredito)
class CartaoCreditoAdmin(admin.ModelAdmin):
    pass


@admin.register(CapitalGiro)
class CapitalGiroAdmin(admin.ModelAdmin):
    pass
