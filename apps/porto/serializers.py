from rest_framework import serializers

from .models import PropostaPorto


class PropostaPortoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropostaPorto
        fields = [
            "id",
            "estado_simulacao",
            "simulado_em",
            "valores_parcelas",
            "mensagem",
        ]
