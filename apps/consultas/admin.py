import easy
from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django_json_widget.widgets import JSONEditorWidget
from validate_docbr import CNPJ
from validate_docbr import CPF

from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        # fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        models.JSONField: {"widget": JSONEditorWidget}
    }

    search_fields = ["entrada"]
    list_filter = ["tipo", AutocompleteFilterFactory("Usuário", "usuario")]
    list_display = ["get_entrada", "tipo", "usuario", "get_mensagem", "modificado_em"]

    @easy.short(desc="mensagem", order="resultado__message", tags=True)
    def get_mensagem(self, obj):
        return obj.resultado["message"]

    @easy.short(desc="entrada", order="entrada", tags=True)
    def get_entrada(self, obj):
        if obj.get_input_type() == "CPF":
            validator = CPF()
            masked = validator.mask(obj.entrada)
            if validator.validate(obj.entrada):
                return masked
        else:
            validator = CNPJ()
            masked = validator.mask(obj.entrada)
            if validator.validate(obj.entrada):
                return masked

        return format_html('<b style="color:red;">{}</b>', masked)
