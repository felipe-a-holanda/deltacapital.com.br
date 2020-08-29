# Create your views here.
import datetime
import re
from urllib.parse import quote

import pytz
import requests
from constance import config
from django.forms import modelform_factory
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from . import constants
from .forms import BasePropostaForm
from apps.delta.helpers import model_to_dict_verbose
from .models import PropostaPorto



PORTO_URL = (
    "https://financeiraportoseguro.com.br/?"
    "menuid=COL-02U75%23%23"
    "portal=1%23%23"
    "corsus=3B501J%23%23"
    "webusrcod=2527707%23%23"
    "usrtip=S%23%23"
    "sesnum=99124634%23%23"
    "cpf=82721351320"
)


def myview(request):
    obj = PropostaPorto.objects.first()
    dic = model_to_dict_verbose(obj, exclude=("id", "stage", "session_hash"))

    # dic = model_to_dict_verbose(self, exclude=("id", "codigo_interno"))
    # send_default_email.delay(dic, "Proposta")
    # msg_plain = render_to_string("delta/emails/email.txt", {"object": dic})
    msg_plain = render_to_string("delta/emails/email.html", {"object": dic})

    return HttpResponse(msg_plain, charset="utf-8")



class PortoView(TemplateView):
    template_name = f"porto/porto.html"

    def rewrite_src(self, text):
        text = re.sub(
            r'script src="(.*)"',
            r'script src="https://financeiraportoseguro.com.br\1"',
            text,
        )
        return text

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        headers = {"Accept-Encoding": "identity"}
        response = requests.get(PORTO_URL, headers=headers)
        porto = self.rewrite_src(response.text)
        context.update({"porto": porto})
        return context


porto_view = PortoView.as_view()





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


class PropostaView(FormView):
    template_name = "porto/proposta/proposta.html"
    proposta = None
    form_class = None

    def _get_stage(self, form=None):
        if self.page:
            stage = self.page
        elif self.proposta:
            stage = self.proposta.stage
        else:
            stage = constants.STAGE_1
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
        from .tasks import get_simulation

        get_simulation.delay(proposta.pk, form.cleaned_data)

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
        form.instance.stage = new_stage
        form.save()  # This will save the underlying instance.
        if new_stage == constants.COMPLETE:
            form.instance.send_mail()
            return redirect(reverse("delta:obrigado"))
        if new_stage == constants.STAGE_2:
            form.instance.simular()
            return redirect(
                reverse("porto:proposta_simulacao", args=(form.instance.pk,))
            )
        # elif new_stage == constants.STAGE_2:
        #    self.run_simulation(proposta, form)
        # else
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

from .constants import STATUS_RECUSADO
from .constants import STATUS_APROVADO
class PropostaSimulacaoView(TemplateView):
    template_name = "porto/proposta/simulacao.html"

    def get_context_data(self, **kwargs):
        context = super(PropostaSimulacaoView, self).get_context_data()
        api_url = reverse("propostaporto-detail", args=[self.kwargs["id"]])
        context["api_url"] = api_url
        context["return_url"] = "/proposta/2/"
        context["returns"] = {STATUS_RECUSADO: reverse("porto:recusado"),
                              STATUS_APROVADO: "/proposta/2/"
                              }
        return context

    pass


proposta_simulacao_view = PropostaSimulacaoView.as_view()


class ObrigadoView(TemplateView):
    template_name = "delta/obrigado.html"


obrigado_view = ObrigadoView.as_view()

class RecusadoView(TemplateView):
    template_name = "porto/proposta/recusado.html"


recusado_view = RecusadoView.as_view()



def load_anos(request):
    ano_fabricacao = request.GET.get('ano')
    ano = int(ano_fabricacao)
    anos_modelo = list(map(str, [ano, ano+1]))

    return render(request, 'porto/ano_modelo_dropdown_list_options.html', {'anos': anos_modelo})