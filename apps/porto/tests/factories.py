from factory.django import DjangoModelFactory

from apps.porto.models import PropostaPorto


class PropostaPortoFactory(DjangoModelFactory):
    class Meta:
        model = PropostaPorto
