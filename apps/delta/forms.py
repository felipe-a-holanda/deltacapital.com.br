from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm


class BaseApplicationForm(ModelForm):
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        field_classes = {
            "moeda": ["valor_do_veiculo", "valor_de_entrada", "renda_mensal_pessoal", "outras_rendas"],
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
        }

        for field in self.visible_fields():
            for k in field_classes:
                if field.name in field_classes[k]:
                    field.field.widget.attrs['class'] = k


        required_fields = self.instance.required_fields
        hidden_fields = self.instance.hidden_fields
        for field in self.fields:
            if field in required_fields:
                self.fields.get(field).required = True  # type:ignore
            if field in hidden_fields:
                self.fields.get(field).widget = HiddenInput()  # type:ignore

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        if len(cpf) < 14:
            raise ValidationError(f"CPF incompleto")
        return cpf

    # class Media:
        # css = {
        #     "all": ("job_application/css/job_application.css",)
        # }
