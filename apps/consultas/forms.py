from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from validate_docbr import CNPJ
from validate_docbr import CPF

from .models import Consulta

SHIFTDATA_API_KEY = settings.SHIFTDATA_API_KEY
SHIFTDATA_BASE_URL = "https://api.shiftdata.com.br"


def only_digits(value):
    if value:
        return "".join([c for c in value if c.isdigit()])


class ConsultaForm(ModelForm):
    class Meta:
        model = Consulta
        fields = ["entrada", "tipo"]

    def clean_entrada(self):
        entrada = self.cleaned_data.get("entrada", None)
        if entrada:
            entrada = only_digits(entrada)
            if not CPF().validate(entrada) and not CNPJ().validate(entrada):
                raise ValidationError("Insira um CPF ou CNPJ válido")
        return entrada

    def clean(self):
        entrada = self.cleaned_data.get("entrada", None)
        tipo = self.cleaned_data.get("tipo", None)
        if entrada and tipo:
            if tipo == "PessoaJuridica":
                if not CNPJ().validate(entrada):
                    raise ValidationError("Insira CNPJ válido")
            else:
                if not CPF().validate(entrada):
                    raise ValidationError("Insira CPF válido")
