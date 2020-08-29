from rest_framework import viewsets

from .models import PropostaPorto
from .serializers import PropostaPortoSerializer


class PropostaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PropostaPorto.objects.all()
    serializer_class = PropostaPortoSerializer
