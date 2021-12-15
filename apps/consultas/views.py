from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.edit import ProcessFormView

from .forms import ConsultaForm
from .models import Consulta


class ConsultaCreateView(
    LoginRequiredMixin,
    SingleObjectTemplateResponseMixin,
    ModelFormMixin,
    ProcessFormView,
):
    model = Consulta
    template_name_suffix = "_form"
    form_class = ConsultaForm

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def clean_entrada(self, entrada):
        if entrada:
            return "".join([c for c in entrada if c.isdigit()])

    def get_object(self, request):
        object = Consulta.objects.filter(
            entrada=self.clean_entrada(request.POST.get("entrada")),
            tipo=request.POST.get("tipo"),
        ).first()
        if object:
            request.session["stored"] = True
            return object
        request.session["stored"] = False
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(request)
        return super().post(request, *args, **kwargs)


class ConsultaDetailView(DetailView):
    model = Consulta

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        tipo = self.kwargs.get("tipo")
        entrada = self.kwargs.get("entrada")

        if tipo is not None and entrada is not None:
            queryset = queryset.filter(tipo=tipo, entrada=entrada)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.first()
        except queryset.model.DoesNotExist:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj


class ConsultaNovaDetailView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = "consultas:detail"

    def get_redirect_url(self, *args, **kwargs):
        consulta = get_object_or_404(
            Consulta, tipo=kwargs["tipo"], entrada=kwargs["entrada"]
        )
        consulta.consultar()
        return super().get_redirect_url(*args, **kwargs)
