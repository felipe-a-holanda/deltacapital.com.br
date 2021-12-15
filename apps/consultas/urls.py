from django.urls import path

from . import views

app_name = "apps.consultas"


urlpatterns = [
    path(
        "resultado/<str:tipo>/<str:entrada>/",
        views.ConsultaDetailView.as_view(),
        name="detail",
    ),
    path(
        "consultar/<str:tipo>/<str:entrada>/",
        views.ConsultaNovaDetailView.as_view(),
        name="consultar",
    ),
    path("", views.ConsultaCreateView.as_view(), name="create"),
]
