import easy
from django.contrib import admin
from django.utils.html import format_html
from .models import Proposta
from django.db import models
from django import  forms
# Register your models here.

from .constants import STATUS_COLORS


def status_colored(obj, field_name="status"):
    return format_html(
        '<b style="color:{};">{}</b>',
        STATUS_COLORS[obj.status],
        getattr(obj, field_name)
    )


@admin.register(Proposta)
class PropostaAdmin(admin.ModelAdmin):
    list_display = ["cliente", "get_cpf_cnpj", "status"]
    list_editable = ["status"]
    list_filter = ("criada_em", "status")

    formfield_overrides = {
        models.DecimalField: {'widget': forms.NumberInput(attrs={'step': 0.6})}
    }

    @easy.short(desc='Cpf/Cnpj', order='cpf_cnpj', tags=True)
    def get_cpf_cnpj(self, obj):
        return status_colored(obj, "cpf_cnpj")
