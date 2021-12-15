from django.contrib import admin

from .models import Consulta


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    search_fields = ["entrada"]
    list_filter = ["tipo", "usuario"]
    list_display = ["tipo", "entrada", "usuario", "modificado_em"]
