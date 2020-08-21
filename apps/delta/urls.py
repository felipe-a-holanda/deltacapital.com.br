from django.urls import path

from .views import capital_de_giro_view
from .views import cartao_view
from .views import current_datetime
from .views import emprestimo_view
from .views import financiamento_view
from .views import home_view
from .views import myview
from .views import obrigado_view
from .views import proposta_simulacao_view
from .views import proposta_view
from .views import whatsapp_view

app_name = "apps.delta"


urlpatterns = [
    path("", home_view, name="home"),
    path("whatsapp", whatsapp_view, name="whatsapp"),
    path("test", myview, name="test"),
    path(
        "financiamento-de-veiculos",
        financiamento_view,
        name="financiamento-de-veiculos",
    ),
    path("capital-de-giro", capital_de_giro_view, name="capital-de-giro"),
    path("cartao-de-credito", cartao_view, name="cartao-de-credito"),
    path("emprestimo-pessoal", emprestimo_view, name="emprestimo-pessoal"),
    path("proposta/", proposta_view, name="proposta"),
    path("proposta/new/", proposta_view, {"new": True}, name="proposta"),
    path(
        "proposta/simulacao/<int:id>/",
        proposta_simulacao_view,
        name="proposta_simulacao",
    ),
    path("proposta/<str:page>/", proposta_view, name="proposta"),
    path("obrigado/", obrigado_view, name="obrigado"),
    path("task/", current_datetime, name="task"),
    # path("<str:slug>/", product_view, name="produto"),
]
