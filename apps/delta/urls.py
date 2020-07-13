from django.urls import path

from .views import home_view
from .views import obrigado_view
from .views import product_view
from .views import proposta_view
from .views import whatsapp_view


app_name = "apps.delta"
urlpatterns = [
    path("", home_view, name="home"),

    path("whatsapp", whatsapp_view, name="whatsapp"),
    path("proposta/", proposta_view, name="proposta"),
    path("proposta/<str:page>/", proposta_view, name="proposta"),
    path("obrigado/", obrigado_view, name="obrigado"),
    path("<str:slug>/", product_view, name="produto"),
]
