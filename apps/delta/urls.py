from django.urls import path

from .views import home_view
from .views import product_view
from .views import whatsapp_view


app_name = "apps.delta"
urlpatterns = [
    path("", home_view, name="home"),
    path("whatsapp", whatsapp_view, name="whatsapp"),
    path("produto/<str:slug>/", product_view, name="produto"),


]

