from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from validate_docbr import CPF

from .models import CapitalGiro
from .models import CartaoCredito
from .models import FinanciamentoVeiculo


cpf_validator = CPF()


class BaseForm(ModelForm):
    field_classes = {}  # type: ignore

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_css()
        self.change_widgets()

    def add_css(self):
        for field in self.visible_fields():
            klasses = []
            for k in self.field_classes:
                if field.name in self.field_classes[k]:
                    klasses.append(k)
            field.field.widget.attrs["class"] = " ".join(klasses)
            field.klass = field.field.widget.attrs["class"]

    def change_widgets(self):
        radio_fields = getattr(self, "radio_fields", [])

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices = field.choices[1:]  # type: ignore

            if field_name in radio_fields:
                field.widget = forms.RadioSelect(choices=field._choices)  # type: ignore


class FinanciamentoVeiculoForm(BaseForm):
    field_classes = {
        "moeda": ["valor_do_veiculo", "entrada"],
        "cpf": ["cpf"],
        "celular": ["telefone"],
    }

    class Meta:
        model = FinanciamentoVeiculo
        fields = "__all__"

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"].strip()
        if cpf_validator.validate(cpf):
            return cpf
        else:
            raise ValidationError("CPF Inválido")


class CartaoCreditoForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    field_classes = {
        "cpf": ["cpf"],
        "email": ["email"],
        "celular": ["telefone"],
        "cep": ["cep"],
        "data": ["data_de_nascimento"],
        "radio-toolbar": ["pessoa", "bandeira", "sexo"],
        "radio-toolbar-horizontal": ["id_pessoa", "pessoa", "bandeira", "sexo"],
        "label-float": [
            "nome",
            "cpf",
            "email",
            "telefone",
            "cep",
            "data_de_nascimento",
            "nome_mae",
            "endereco",
        ],
        "label-float form-group": ["vencimento"],
    }
    # Verificar
    radio_fields = ["pessoa", "bandeira", "sexo"]

    class Meta:
        model = CartaoCredito
        fields = ["nome", "cpf", "email", "nome"]


class CapitalGiroForm(BaseForm):
    field_classes = {
        "moeda": ["valor_emprestimo"],
        "cnpj": ["cnpj"],
        "email": ["email"],
        "celular": ["telefone"],
    }

    class Meta:
        model = CapitalGiro
        fields = "__all__"
