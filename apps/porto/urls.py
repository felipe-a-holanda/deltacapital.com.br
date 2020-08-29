from django.urls import path

from .views import recusado_view
from .views import proposta_simulacao_view
from .views import proposta_view
from .views import load_anos

app_name = "apps.porto"


urlpatterns = [

    path("proposta/", proposta_view, name="proposta"),
    path("proposta/new/", proposta_view, {"new": True}, name="proposta"),
    path(
        "proposta/simulacao/<int:id>/",
        proposta_simulacao_view,
        name="proposta_simulacao",
    ),
    path("proposta/<str:page>/", proposta_view, name="proposta"),
    path("obrigado-pelo-interesse/", recusado_view, name="recusado"),
    path("ajax/load_anos/", load_anos, name="ajax_load_anos"),
]
