from django.urls import path

from . import views

app_name = "apps.shiftdata"


urlpatterns = [
    path("pesquisa/", views.ShiftDataFormView.as_view(), name="form"),
    path("resultado/", views.ShiftDataResultView.as_view(), name="result"),
]
