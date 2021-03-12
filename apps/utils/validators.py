from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_cpf(value):

    if not CPF().validate(value):
        raise ValidationError(
            _('CPF %(value)s inválido'),
            params={'value': value},
        )