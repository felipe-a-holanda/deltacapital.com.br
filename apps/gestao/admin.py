import easy
from django import forms
from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from .constants import STATUS_COLORS
from .models import Proposta

# Register your models here.


def status_colored(obj, field_name="status"):
    return format_html(
        '<b style="color:{};">{}</b>',
        STATUS_COLORS[obj.status],
        getattr(obj, field_name),
    )


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ["cliente", "get_cpf_cnpj", "status"]
    list_editable = ["status"]
    list_filter = ("criada_em", "status")

    formfield_overrides = {
        models.DecimalField: {"widget": forms.NumberInput(attrs={"step": 0.6})}
    }

    readonly_fields = [
        "user",
        "proposta_porto",
        "valor_financiado",
        "valor_comissao",
        "valor_comissao_operador",
        "valor_comissao_campanha",
        "valor_comissao_liquido",
    ]

    @easy.short(desc="Cpf/Cnpj", order="cpf_cnpj", tags=True)
    def get_cpf_cnpj(self, obj):
        return status_colored(obj, "cpf_cnpj")

    def get_form(self, request, obj=None, **kwargs):
        # here insert/fill the current user name or id from request
        if obj is not None:
            obj.user = request.user
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
