from django.urls import path

from .views import load_anos
from .views import proposta_simulacao_view
from .views import proposta_view
from .views import recusado_view

app_name = "apps.porto"

from .views import *
urlpatterns = [
    path("proposta/", PropostaCreateView.as_view(), name="proposta-create"),
    path("proposta/<int:pk>/<int:page>/", PropostaUpdateView.as_view(), name="proposta-update"),
    #path("proposta/<int:id>/", proposta_view, name="proposta"),
    #path("proposta/<int:id>/<str:page>/", proposta_view, name="proposta"),
    #path("proposta/new/", proposta_view, {"new": True}, name="proposta"),
    path(
        "proposta/simulacao/<int:pk>/",
        proposta_simulacao_view,
        name="proposta-simulacao",
    ),
   # path("proposta/<str:page>/", proposta_view, name="proposta"),
    path("obrigado-pelo-interesse/", recusado_view, name="proposta-recusada"),
    path("proposta/obrigado/", obrigado_view, name="proposta-fim"),
    path("ajax/load_anos/", load_anos, name="ajax_load_anos"),
]
