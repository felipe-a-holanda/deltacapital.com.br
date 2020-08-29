from django.contrib import admin

from .models import CapitalGiro
from .models import CartaoCredito
from .models import FinanciamentoVeiculo


@admin.register(FinanciamentoVeiculo)
class FinanciamentoVeiculoAdmin(admin.ModelAdmin):
    pass


@admin.register(CartaoCredito)
class CartaoCreditoAdmin(admin.ModelAdmin):
    pass


@admin.register(CapitalGiro)
class CapitalGiroAdmin(admin.ModelAdmin):
    pass
