from django.urls import path

from .views import load_anos
from .views import obrigado_view
from .views import proposta_simulacao_view
from .views import PropostaCreateView
from .views import PropostaUpdateView
from .views import PropostaSelectView
from .views import recusado_view
from .views import test_email


app_name = "apps.porto"

urlpatterns = [
    path("cdcveiculos/", PropostaSelectView.as_view(), name="proposta-create"),
    path("cdcveiculos-pf/", PropostaCreateView.as_view(), name="proposta-pf"),
    path("cdcveiculos-pj/", PropostaCreateView.as_view(), name="proposta-pj"),
    path(
        "cdcveiculos/<int:pk>/<int:page>/",
        PropostaUpdateView.as_view(),
        name="proposta-update",
    ),
    # path("proposta/<int:id>/", proposta_view, name="proposta"),
    # path("proposta/<int:id>/<str:page>/", proposta_view, name="proposta"),
    # path("proposta/new/", proposta_view, {"new": True}, name="proposta"),
    path(
        "cdcveiculos/simulacao/<int:pk>/",
        proposta_simulacao_view,
        name="proposta-simulacao",
    ),
    # path("proposta/<str:page>/", proposta_view, name="proposta"),
    path("obrigado-pelo-interesse/", recusado_view, name="proposta-recusada"),
    path("cdcveiculos/<int:pk>/obrigado/", obrigado_view, name="proposta-fim"),
    path("ajax/load_anos/", load_anos, name="ajax_load_anos"),
    path("email/<int:pk>/", test_email),
]
