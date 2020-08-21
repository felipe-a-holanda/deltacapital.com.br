from rest_framework import viewsets
from .models import Proposta
from .serializers import PropostaSerializer


class PropostaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proposta.objects.all()
    serializer_class = PropostaSerializer