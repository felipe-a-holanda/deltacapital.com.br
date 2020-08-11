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
from .forms import CapitalGiroForm
from .forms import CartaoCreditoForm
from .forms import FinanciamentoVeiculoForm
from .helpers import model_to_dict_verbose
from .models import CapitalGiro
from .models import CartaoCredito
from .models import FinanciamentoVeiculo
from .models import Proposta
from .tasks import get_simulation
from .tasks import send_default_email


class HomeView(TemplateView):
    template_name = "delta/index.html"


home_view = HomeView.as_view()

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
    obj = Proposta.objects.first()
    dic = model_to_dict_verbose(obj, exclude=("id", "stage", "session_hash"))

    # dic = model_to_dict_verbose(self, exclude=("id", "codigo_interno"))
    # send_default_email.delay(dic, "Proposta")
    # msg_plain = render_to_string("delta/emails/email.txt", {"object": dic})
    msg_plain = render_to_string("delta/emails/email.html", {"object": dic})

    return HttpResponse(msg_plain, charset="utf-8")


class PortoView(TemplateView):
    template_name = f"delta/porto.html"

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


class ProductView(TemplateView):
    def get_template_names(self):
        slug = self.kwargs["slug"]
        template = f"delta/produtos/{slug}.html"
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise Http404
        return template


product_view = ProductView.as_view()


class WhatsappRedirectView(RedirectView):
    permanent = False

    def get_whatsapp_url(self, phone, text):
        phone = "".join([c for c in phone if c.isdigit()])

        text = quote(text)
        url = f"https://api.whatsapp.com/send?phone={phone}&text={text}"
        return url

    def get_redirect_url(self, *args, **kwargs):
        phone = config.WHATSAPP_NUMERO
        text = config.WHATSAPP_MENSAGEM
        return self.get_whatsapp_url(phone, text)


whatsapp_view = WhatsappRedirectView.as_view()


def get_obj_from_hash(session_hash):
    # Find and return an unexpired, not-yet-completed JobApplication
    # with a matching session_hash, or None if no such object exists.
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
    max_age = 2 * 60 * 60  # Or make this a setting in "settings.py"
    exclude_before = now - datetime.timedelta(seconds=max_age)
    return (
        Proposta.objects.filter(
            session_hash=session_hash, criado_em__gte=exclude_before
        )
        .exclude(stage=constants.COMPLETE)
        .first()
    )


class PropostaView(FormView):
    template_name = "delta/proposta/proposta.html"
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
        # elif new_stage == constants.STAGE_2:
        #    self.run_simulation(proposta, form)
        # else
        return redirect(reverse("delta:proposta", args=(new_stage,)))

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

        fields = Proposta.get_fields_by_stage(stage)
        # Use those fields to dynamically create a form with "modelform_factory"
        form = modelform_factory(Proposta, BasePropostaForm, fields)
        self.fill_initial_fields(form)
        return form

    def get_form_kwargs(self):
        # Make sure Django uses the same JobApplication instance we've already been
        # working on. Otherwise it will instantiate a new one after every submit.
        kwargs = super().get_form_kwargs()

        kwargs["instance"] = self.proposta
        return kwargs


proposta_view = PropostaView.as_view()


class ObrigadoView(TemplateView):
    template_name = "delta/obrigado.html"


obrigado_view = ObrigadoView.as_view()


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    # browser_send_form({"Valor":"123456,78", "EntradaOutro":"999", "CPF":"03715358165"})
    get_simulation({"Valor": "123456,78", "EntradaOutro": "999", "CPF": "82721351320"})
    return HttpResponse(html)


class ProductCreate(CreateView):
    # fields = "__all__"
    success_url = reverse_lazy("delta:obrigado")
    subject = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object:  # type: ignore
            self.send_email(self.object)  # type: ignore
        return response

    def send_email(self, object):
        dic = model_to_dict_verbose(object)
        send_default_email.delay(dic, self.subject)


class FinanciamentoVeiculoCreate(ProductCreate):
    model = FinanciamentoVeiculo
    form_class = FinanciamentoVeiculoForm
    template_name = "delta/produtos/financiamento-de-veiculos.html"
    subject = "Financiamento de Veiculo: "


financiamento_view = FinanciamentoVeiculoCreate.as_view()


class CartaoCreditoCreate(ProductCreate):
    model = CartaoCredito
    form_class = CartaoCreditoForm
    template_name = "delta/produtos/cartao-de-credito.html"
    subject = "Cartão de Crédito: "


cartao_view = CartaoCreditoCreate.as_view()


class CapitalGiroCreate(CreateView):
    model = CapitalGiro
    form_class = CapitalGiroForm
    template_name = "delta/produtos/capital-de-giro.html"
    subject = "Capital de Giro: "


capital_de_giro_view = CapitalGiroCreate.as_view()


class EmprestimoRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return "https://www.geru.com.br/?utm_source=DeltaCapital&utm_medium=DeltaCapital&utm_content=DeltaCapital"


emprestimo_view = EmprestimoRedirectView.as_view()
