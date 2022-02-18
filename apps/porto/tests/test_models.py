import pytest

from apps.porto.tests.factories import PropostaPortoFactory

pytestmark = pytest.mark.django_db


def test_email_format():
    proposta = PropostaPortoFactory()
    email_dic = proposta.format_email()

    print(email_dic)
