import re

from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from validate_docbr import CNPJ
from validate_docbr import CPF

from apps.consultas.shiftdata_api import ShiftDataAPI
from apps.users.forms import User


class Consulta(models.Model):
    TIPOS = (
        ("PessoaFisica", "Pessoa Física"),
        ("PessoaJuridica", "Pessoa Jurídica"),
        ("VinculosEmpresariais", "Vínculos Empresariais"),
        ("ParticipacaoEmpresarial", "Participação Empresarial"),
    )

    entrada = models.CharField(max_length=18, validators=[MinLengthValidator(11)])
    tipo = models.CharField(max_length=100, choices=TIPOS)
    resultado = models.JSONField(null=True, blank=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(blank=True, default=timezone.now)
    modificado_em = models.DateTimeField(blank=True, default=timezone.now)

    def __str__(self):
        return f"{self.tipo} ({self.entrada})"

    def get_absolute_url(self):
        return reverse("consultas:detail", args=(self.tipo, self.entrada))

    def get_url_consulta(self):
        return reverse("consultas:consultar", args=(self.tipo, self.entrada))

    def get_input_type(self):
        if self.tipo == "PessoaJuridica":
            return "CNPJ"
        return "CPF"

    def get_formatted_input(self):
        if self.get_input_type() == "CNPJ":
            return CNPJ().mask(self.entrada)
        return CPF().mask(self.entrada)

    def get_result(self):
        def parse_key(key):
            if key in ["CPF"]:
                return key
            return " ".join(re.findall("[A-Z][^A-Z]*", key))

        if self.resultado and "result" in self.resultado:
            result = self.resultado["result"]
            if result:
                return {parse_key(k): v for k, v in result.items()}
            return self.resultado

    def consultar(self):
        resultado = ShiftDataAPI().call_endpoint(self.tipo, self.entrada)
        self.resultado = resultado
        self.save()

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            resultado = ShiftDataAPI().call_endpoint(self.tipo, self.entrada)
            self.resultado = resultado

        return super().save(*args, **kwargs)
