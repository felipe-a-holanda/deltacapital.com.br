from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import capital_de_giro_view
from .views import cartao_view
from .views import emprestimo_view
from .views import financiamento_view
from .views import home_view
from .views import obrigado_view
from .views import whatsapp_view

app_name = "apps.delta"


urlpatterns = [
    path("", home_view, name="home"),
    path("whatsapp", whatsapp_view, name="whatsapp"),
    path(
        "financiamento-de-veiculos",
        financiamento_view,
        name="financiamento-de-veiculos",
    ),
    path("capital-de-giro", capital_de_giro_view, name="capital-de-giro"),
    path("cartao-de-credito", cartao_view, name="cartao-de-credito"),
    path("emprestimo-pessoal", emprestimo_view, name="emprestimo-pessoal"),
    path("obrigado/", obrigado_view, name="obrigado"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
