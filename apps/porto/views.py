import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import modelform_factory
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from . import constants
from .constants import COMPLETE
from .constants import STAGE_1
from .constants import STAGE_2
from .constants import STATUS_EM_DIGITACAO
from .constants import STATUS_ERRO
from .constants import STATUS_NAO_SIMULADO
from .constants import STATUS_PRE_RECUSADO
from .forms import BasePropostaForm
from .models import PropostaPorto


def get_obj_from_hash(session_hash):
    # Find and return an unexpired, not-yet-completed JobApplication
    # with a matching session_hash, or None if no such object exists.
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    max_age = 2 * 60 * 60  # Or make this a setting in "settings.py"
    exclude_before = now - datetime.timedelta(seconds=max_age)
    return (
        PropostaPorto.objects.filter(
            session_hash=session_hash, criado_em__gte=exclude_before
        )
        .exclude(stage=constants.COMPLETE)
        .first()
    )


class PropostaCreateView(LoginRequiredMixin, CreateView):
    template_name = "porto/proposta/proposta.html"
    model = PropostaPorto
    fields = PropostaPorto.FIELDS[STAGE_1]

    def form_valid(self, form):
        response = super(PropostaCreateView, self).form_valid(form)
        self.object.user = self.request.user  # type: ignore
        self.object.save()  # type: ignore
        return response

    def get_form_class(self):
        fields = PropostaPorto.get_fields_by_stage(STAGE_1)
        form = modelform_factory(PropostaPorto, BasePropostaForm, fields)
        return form

    def get_success_url(self):
        return reverse('porto:proposta-update',
                       kwargs={'pk': self.object.pk, 'page': '2'})
        #return reverse(
        #    "porto:proposta-simulacao", kwargs={"pk": self.object.pk}  # type: ignore
        #)



class PropostaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "porto/proposta/proposta.html"
    model = PropostaPorto
    fields = PropostaPorto.FIELDS[STAGE_1]

    def get_form_class(self):
        page = self.kwargs.get("page", STAGE_1)
        fields = PropostaPorto.get_fields_by_stage(page)
        form = modelform_factory(PropostaPorto, BasePropostaForm, fields)
        return form

    def dispatch(self, request, *args, **kwargs):
        # Check permissions for the request.user here
        page = kwargs.get("page", 1)
        self.object = self.get_object()
        self.object.pagina = page  # type: ignore
        self.object.save()
        if self.object.user != request.user:  # type: ignore
            raise PermissionDenied()

        self.fields = PropostaPorto.FIELDS[page]
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PropostaUpdateView, self).get_context_data(**kwargs)
        page = self.kwargs.get("page", 1)
        back_stage = page - 1

        if back_stage > 0:
            context["current_stage"] = page
            context["back_stage"] = back_stage

        return context

    def get_success_url(self):
        page = self.kwargs.get("page", 1)
        next = page + 1
        if next == COMPLETE:

            return reverse("porto:proposta-fim", kwargs={"pk": self.object.pk})
        return reverse(
            "porto:proposta-update", kwargs={"pk": self.object.pk, "page": next}
        )


# Old:
class PropostaView(LoginRequiredMixin, FormView):
    template_name = "porto/proposta/proposta.html"
    proposta = None
    form_class = None

    def _get_stage(self, form=None):
        if self.page:
            stage = self.page
        elif self.proposta:
            stage = self.proposta.pagina
        else:
            stage = constants.STAGE_1
        print("pagina=", stage)
        return stage

    def _get_back_stage(self):
        current_stage = self._get_stage()
        i = constants.STAGE_ORDER.index(current_stage)
        return constants.STAGE_ORDER[i - 1] if i - 1 >= 0 else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proposta"] = self.proposta
        context["session_hash"] = self.session_hash
        context["current_stage"] = self._get_stage()
        context["back_stage"] = self._get_back_stage
        return context

    def dispatch(self, request, *args, **kwargs):
        session_hash = request.session.get("session_hash", None)
        self.session_hash = session_hash
        self.page = kwargs.pop("page", None)
        # Get the job application for this session. It could be None.
        if "new" not in kwargs:
            self.proposta = get_obj_from_hash(session_hash)
            print("proposta=", self.proposta)

        else:
            self.proposta = None
        # Attach the request to "self" so "form_valid()" can access it below.
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def run_simulation(self, proposta, form):
        from .tasks import run_simulation

        run_simulation.delay(proposta.pk, form.cleaned_data)

    def get_user(self):
        u = self.request.GET.get("u")
        print(u)

    def form_valid(self, form):
        # This data is valid, so set this form's session hash in the session.
        self.request.session["session_hash"] = form.instance.session_hash
        # current_stage = form.cleaned_data.get("stage")
        current_stage = self._get_stage()
        self.get_user()

        # Get the next stage after this one.

        new_stage = constants.STAGE_ORDER[
            constants.STAGE_ORDER.index(current_stage) + 1
        ]
        form.instance.pagina = new_stage
        form.save(request=self.request)  # This will save the underlying instance.
        if new_stage == constants.COMPLETE:
            form.instance.send_mail()
            return redirect(reverse("delta:obrigado"))
        #if new_stage == constants.STAGE_2:
        #    form.instance.simular()
        #    return redirect(
        #        reverse("porto:proposta_simulacao", args=(form.instance.pk,))
        #    )

        return redirect(reverse("porto:proposta", args=(new_stage,)))

    def fill_initial_fields(self, form):
        d = {"o": "nome_operador", "v": "valor_do_veiculo"}
        for key, value in self.request.GET.items():
            k = d.get(key, key)
            if k in form.base_fields:
                form.base_fields[k].initial = value

    def get_form_class(self):
        # If we found a job application that matches the session hash, look at
        # its "stage" attribute to decide which stage of the application we're
        # on. Otherwise assume we're on stage 1.
        if self.page:
            stage = self.page
        elif self.proposta:
            stage = self.proposta.stage
        else:
            stage = constants.STAGE_1

        # stage = self.proposta.stage if self.proposta else constants.STAGE_1
        # Get the form fields appropriate to that stage.

        fields = PropostaPorto.get_fields_by_stage(stage)
        # Use those fields to dynamically create a form with "modelform_factory"
        form = modelform_factory(PropostaPorto, BasePropostaForm, fields)
        self.fill_initial_fields(form)
        return form

    def get_form_kwargs(self):
        # Make sure Django uses the same JobApplication instance we've already been
        # working on. Otherwise it will instantiate a new one after every submit.
        kwargs = super().get_form_kwargs()

        kwargs["instance"] = self.proposta
        return kwargs


proposta_view = PropostaView.as_view()


class PropostaSimulacaoView(DetailView):
    template_name = "porto/proposta/simulacao.html"
    model = PropostaPorto

    def get(self, request, *args, **kwargs):
        response = super(PropostaSimulacaoView, self).get(request, *args, **kwargs)
        self.object.simular()  # type: ignore
        return response

    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        context = super(PropostaSimulacaoView, self).get_context_data()
        api_url = reverse("propostaporto-detail", args=[pk])
        next_url = reverse("porto:proposta-update", args=[pk, STAGE_2])
        recusado_url = reverse("porto:proposta-recusada")

        context["api_url"] = api_url
        context["return_url"] = next_url
        context["returns"] = {
            STATUS_NAO_SIMULADO: next_url,
            STATUS_ERRO: next_url,
            STATUS_PRE_RECUSADO: recusado_url,
            STATUS_EM_DIGITACAO: next_url,
        }
        return context


proposta_simulacao_view = PropostaSimulacaoView.as_view()


class ObrigadoView(DetailView):
    template_name = "porto/obrigado.html"
    model = PropostaPorto

    def get(self, request, *args, **kwargs):
        response = super(ObrigadoView, self).get(request, *args, **kwargs)

        self.object.finish()  # type: ignore
        return response


obrigado_view = ObrigadoView.as_view()


class RecusadoView(TemplateView):
    template_name = "porto/proposta/recusado.html"


recusado_view = RecusadoView.as_view()


def load_anos(request):
    ano_fabricacao = request.GET.get("ano")
    ano = int(ano_fabricacao)
    anos_modelo = list(map(str, [ano, ano + 1]))

    return render(
        request, "porto/ano_modelo_dropdown_list_options.html", {"anos": anos_modelo}
    )


def test_email(request, pk):
    from django.template.loader import render_to_string
    from django.http import HttpResponse
    from apps.delta.helpers import model_to_dict_verbose

    print("pk=", pk)
    object = PropostaPorto.objects.get(pk=pk)
    dic = model_to_dict_verbose(object, exclude=["id"] + object.hidden_fields)
    email = render_to_string("delta/emails/email.html", {"object": dic})
    return HttpResponse(email)


class PropostaSelectView(LoginRequiredMixin, TemplateView):
    template_name = "porto/proposta/proposta-select.html"