import datetime
from collections import defaultdict
from validate_docbr import CPF
from django import forms
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm

from . import constants


class DeltaRadioSelect(forms.widgets.RadioSelect):
    template_name = "project/widgets/filter.html"


class ReadOnlyText(forms.TextInput):
    input_type = "text"

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        return value


def get_value_prazo(n, prazo, valores):
    print(n, prazo, valores)
    x = [i for i in valores if n in i]
    return x[0] if x else prazo


class BaseForm(ModelForm):
    field_classes = {}  # type: ignore

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.change_widgets()
        self.customize_widgets()
        self.add_css()

    def add_css(self):
        for field in self.visible_fields():
            klasses = []
            for k in self.field_classes:
                if field.name in self.field_classes[k]:
                    klasses.append(k)
            field.field.widget.attrs["class"] = " ".join(klasses)
            field.klass = field.field.widget.attrs["class"]

    def get_choices_ano(self):
        year = datetime.datetime.now().year
        years = list(range(year, year - (constants.ANOS + 1), -1))
        choices = [(str(year), str(year)) for year in years]
        return choices

    def customize_widgets(self):
        for field_name in self.fields:
            field = self.fields[field_name]
            if field_name == "ano_de_fabricacao":
                field.widget = forms.Select(choices=self.get_choices_ano())
            elif field_name == "ano_do_modelo":
                field.widget = forms.Select(choices=self.get_choices_ano())
            elif field_name == "motor":
                field.widget = forms.TextInput(
                    attrs={"placeholder": "1.0, 1.6, 2.0..."}
                )
            elif field_name == "placa":
                field.widget = forms.TextInput(
                    attrs={"maxlength": constants.VALIDATE_PLACA_MAX}
                )
            elif field_name == "renavam":
                field.widget = forms.TextInput(
                    attrs={"maxlength": constants.VALIDATE_RENAVAM_MAX}
                )
            elif field_name == "chassi":
                field.widget = forms.TextInput(
                    attrs={"maxlength": constants.VALIDATE_CHASSI_MAX}
                )

    def change_widgets(self):
        required_fields = getattr(self.instance, "required_fields", [])
        radio_fields = getattr(self.instance, "radio_fields", [])
        hidden_fields = getattr(self.instance, "hidden_fields", [])
        readonly_fields = getattr(self.instance, "readonly_fields", [])

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field, forms.TypedChoiceField):
                field.choices = field.choices[1:]  # type:ignore
            if field_name in required_fields:
                field.required = True  # type:ignore
            if field_name in hidden_fields:
                field.widget = HiddenInput()  # type:ignore
            if field_name in readonly_fields:
                field.widget.attrs['readonly'] = True
            if field_name in radio_fields:
                field.widget = forms.RadioSelect(choices=field._choices)  # type: ignore
            if field_name == "prazo":
                if self.instance and self.instance.valores_parcelas:
                    valores = eval(self.instance.valores_parcelas)

                    choices = [(x, f"{x} x R$ {v}") for x, v in valores]

                    field.widget = forms.RadioSelect(choices=choices)  # type: ignore


class BasePropostaForm(BaseForm):
    required_css_class = "required"
    field_classes = {
        "moeda": [
            "valor_do_veiculo",
            "valor_de_entrada",
            "renda_mensal_pessoal",
            "outras_rendas",
        ],
        "label-float": [
            "valor_do_veiculo", 
            "valor_de_entrada", 
            "valor_financiado", 
            "cpf",
            "nome",
            "data_de_nascimento",
            "numero_do_rg",
            "orgao_expedidor",
            "nome_da_mae",
            "local_de_nascimento",
            "uf_de_nascimento",
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "telefone_fixo",
            "celular",
            "email",
            "renda_mensal_pessoal",
            "cep_da_empresa",
            "endereco_comercial",
            "numero_empresa",
            "complemento_empresa",
            "bairro_empresa",
            "cidade_empresa",
            "uf_empresa",
            "inicio_da_atividade",
            "telefone_fixo_da_empresa",
            "tempo_de_empresa",
            "razao_social_da_empresa",
            "cnpj_da_empresa",
            "profissao_liberal",
            "profissao_assalariado",
            "tempo_de_atividade",
            "tempo_de_aposentadoria",
            "outras_rendas",
            "ano_de_fabricacao",
            "ano_do_modelo",
            "marca",
            "modelo",
            "versao",
            "combustivel",
            "cambio",
            "motor",
            "cor",
            "login",
            "placa",
            "renavam",
            "chassi",
            "cnpj",
            
        ],
        "cpf": ["cpf"],
        "cnpj": ["cnpj_da_empresa"],
        "data": ["data_de_nascimento", "inicio_da_atividade"],
        "cep": ["cep", "cep_da_empresa"],
        "celular": ["celular"],
        "telefone": ["telefone_fixo", "telefone_fixo_da_empresa"],
        "email": ["email"],
        "numero": [
            "numero",
            "numero_empresa",
            "tempo_de_empresa",
            "tempo_de_atividade",
            "tempo_de_aposentadoria",
        ],
        "radio-toolbar": ["prazo", "sexo", "tipo_de_renda", "dados_placa"],
        "radio-toolbar-vertical": ["prazo", "tipo_de_renda"],
        "radio-toolbar-horizontal": ["sexo", "dados_placa"],
        "autofill__cep_1": ["cep"],
        "autofill__rua_1": ["endereco"],
        "autofill__bairro_1": ["bairro"],
        "autofill__cidade_1": ["cidade"],
        "autofill__uf_1": ["uf"],
        "autofill__cep_2": ["cep_da_empresa"],
        "autofill__rua_2": ["endereco_comercial"],
        "autofill__bairro_2": ["bairro_empresa"],
        "autofill__cidade_2": ["cidade_empresa"],
        "autofill__uf_2": ["uf_empresa"],
        "conditional": [
            "profissao",
            "cep_da_empresa",
            "endereco_comercial",
            "numero_empresa",
            "numero_empresa",
            "complemento_empresa",
            "bairro_empresa",
            "cidade_empresa",
            "uf_empresa",
            "inicio_da_atividade",
            "telefone_fixo_da_empresa",
            "tempo_de_empresa",
            "razao_social_da_empresa",
            "cnpj_da_empresa",
            "tempo_de_atividade",
            "tempo_de_aposentadoria",
        ],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_conditional_fields()

    def save(self, commit=True, request=None):
        return super().save(commit=commit)

    def config_conditional_fields(self):
        endereco_comercial = [
            "cep_da_empresa",
            "endereco_comercial",
            "numero_empresa",
            "complemento_empresa",
            "bairro_empresa",
            "cidade_empresa",
            "uf_empresa",
            "telefone_fixo_da_empresa",
            "razao_social_da_empresa",
        ]

        conditional_fields = {
            "tipo_de_renda": {
                "assalariado": ["profissao_assalariado"]
                + endereco_comercial
                + ["tempo_de_empresa"],
                "autnomo": ["profissao_liberal", "tempo_de_atividade"],
                "empresario": ["inicio_da_atividade"]
                + endereco_comercial
                + ["cnpj_da_empresa"],
                "aposentado": ["tempo_de_aposentadoria"],
            },
            "dados_placa": {"Sim": ["placa", "renavam", "chassi"]},
        }
        field_types = defaultdict(set)
        source_fields = {}
        for source_field in conditional_fields:
            for tipo_de_renda, fields in conditional_fields[source_field].items():
                for field in fields:
                    field_types[field].add(tipo_de_renda)
                    source_fields[field] = source_field

        for field in self.visible_fields():
            if field.name in field_types:  # type: ignore
                types = field_types[field.name]  # type: ignore
                source = source_fields[field.name]  # type: ignore
                cond = " || ".join([f"[name={source}] == {type}" for type in types])
                field.field.widget.attrs["data-cond"] = cond  # type: ignore
                field.data_cond = cond  # type: ignore

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "").strip()
        cpf_validator = CPF()
        if cpf_validator.validate(cpf):
            return cpf
        else:
            raise ValidationError("CPF Inválido")

