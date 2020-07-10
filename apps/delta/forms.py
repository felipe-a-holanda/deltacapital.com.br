from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from IPython import embed
from . import constants
from .models import Proposta

class DeltaRadioSelect(forms.widgets.RadioSelect):
    template_name = 'project/widgets/filter.html'


class ReadOnlyText(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        return value



class BaseApplicationForm(ModelForm):
    required_css_class = 'required'

    #sexo = forms.ChoiceField(widget=forms.RadioSelect, choices=(("Masculino", "Masculino"), ("Feminino", "Feminino")))
    #comment = forms.CharField(widget=ReadOnlyText, label='comment', help_text="<p>beleza</p>")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.change_widgets()
        self.add_css_classes()
        #self.add_groups()


    def add_css_classes(self):
        field_classes = {
            "moeda": ["valor_do_veiculo", "valor_de_entrada", "renda_mensal_pessoal",
                      "outras_rendas"],
            "cpf": ["cpf"],
            "cnpj": ["cnpj_da_empresa"],
            "data": ["data_de_nascimento"],
            "cep": ["cep", "cep_da_empresa"],
            "celular": ["celular"],
            "telefone": ["telefone_fixo", "telefone_fixo_da_empresa"],
            "email": ["email"],
            "numero": ["numero",
                       "numero_empresa",
                       "inicio_da_atividade",
                       "tempo_de_empresa",
                       "tempo_de_atividade",
                       "tempo_de_aposentadoria",
                       "ano_de_fabricacao",
                       "ano_do_modelo"],


            "radio-toolbar": ["prazo", "sexo", "tipo_de_renda"],
            "radio-toolbar-vertical": ["prazo", "tipo_de_renda"],
            "radio-toolbar-horizontal": ["sexo"],

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

            "conditional": ["profissao",
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
                            ]
            }
        conditional_fields = {
                "tipo_de_renda": {
                    "assalariado": ["profissao"],
                    "autonomo": ["profissao"],
                    "empresario": ["cep_da_empresa", "endereco_comercial"],
                    "aposentado": [],

                }
            }


        data_cond_value_list = defaultdict(list)
        data_cond_option = {}
        for option in conditional_fields:
            for value in conditional_fields[option]:
                for field in conditional_fields[option][value]:
                    data_cond_value_list[field].append(value)
                    data_cond_option[field] = option
        data_cond_value = {field: " ".join(values) for field, values in data_cond_value_list.items()}




        for field in self.visible_fields():
            klasses = []
            for k in field_classes:
                if field.name in field_classes[k]:
                    klasses.append(k)
            field.field.widget.attrs['class'] = " ".join(klasses)
            field.klass = field.field.widget.attrs['class']

            if field.name in data_cond_option:
                field.field.widget.attrs['data-cond-option'] = data_cond_option[field.name]
                field.field.widget.attrs['data-cond-value'] = data_cond_value[field.name]

    def add_groups(self):
        visible_fields = {field.name: field for field in self.visible_fields()}
        field_stage = {field:stage for stage, stage_fields in Proposta.FIELDS.items() for field in stage_fields}

        for field_name, field in visible_fields.items():
            field.group = field_stage[field_name]


    def change_widgets(self):
        required_fields = self.instance.required_fields
        radio_fields = self.instance.radio_fields
        hidden_fields = self.instance.hidden_fields
        for field in self.fields:
            if field in required_fields:
                self.fields.get(field).required = True  # type:ignore
            if field in hidden_fields:
                self.fields.get(field).widget = HiddenInput()  # type:ignore
            if field in radio_fields:
                #embed()
                f = self.fields.get(field)
                f.widget = forms.RadioSelect(choices=f._choices)

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        if len(cpf) < 14:
            raise ValidationError(f"CPF incompleto")
        return cpf

    # class Media:
        # css = {
        #     "all": ("job_application/css/job_application.css",)
        # }
