from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm
from django import forms


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

        self.config_conditional_fields()




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


        for field in self.visible_fields():
            klasses = []
            for k in field_classes:
                if field.name in field_classes[k]:
                    klasses.append(k)
            field.field.widget.attrs['class'] = " ".join(klasses)
            field.klass = field.field.widget.attrs['class']


    def config_conditional_fields(self):
        endereco_comercial = ["cep_da_empresa", "endereco_comercial", "numero_empresa", "complemento_empresa", "bairro_empresa", "cidade_empresa", "uf_empresa", "telefone_fixo_da_empresa", "razao_social_da_empresa"]

        conditional_fields = {
            "tipo_de_renda": {
                "assalariado": ["profissao_assalariado"] + endereco_comercial + ["tempo_de_empresa"],
                "autonomo": ["profissao_liberal", "tempo_de_atividade"],
                "empresario": ["inicio_da_atividade"] + endereco_comercial +["cnpj_da_empresa"],
                "aposentado": ["tempo_de_aposentadoria"],
            },
            "dados_placa": {
                "Sim": ["placa", "renavam", "chassi"]
            }
        }
        field_types = defaultdict(set)
        source_fields = {}
        for source_field in conditional_fields:
            for tipo_de_renda, fields in conditional_fields[source_field].items():
                for field in fields:
                    field_types[field].add(tipo_de_renda)
                    source_fields[field] = source_field

        for field in self.visible_fields():
            if field.name in field_types:
                types = field_types[field.name]
                source = source_fields[field.name]
                cond = " || ".join([f"[name={source}] == {type}" for type in types])
                field.field.widget.attrs['data-cond'] = cond
                field.data_cond = cond




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
