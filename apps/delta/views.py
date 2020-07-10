# Create your views here.
import datetime
from urllib.parse import quote

import pytz
from constance import config
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from IPython import embed

from . import constants
from .forms import BaseApplicationForm
from .models import Proposta


class HomeView(TemplateView):
    template_name = "delta/index.html"


home_view = HomeView.as_view()


class ProductView(TemplateView):
    def get_template_names(self):
        slug = self.kwargs["slug"]
        template = f"delta/products/{slug}.html"
        try:
            get_template(template)
        except TemplateDoesNotExist:
            raise Http404
        return template


product_view = ProductView.as_view()


class WhatsappRedirectView(RedirectView):
    permanent = False

    def get_whatsapp_url(self, phone, text):
        phone.replace(" ", "")
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
    max_age = 24 * 60 * 60  # Or make this a setting in "settings.py"
    exclude_before = now - datetime.timedelta(seconds=max_age)
    return (
        Proposta.objects.filter(
            session_hash=session_hash, enviado_em__gte=exclude_before
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
        return constants.STAGE_ORDER[i-1] if i-1 >= 0 else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_stage'] = self._get_back_stage
        return context

    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        session_hash = request.session.get("session_hash", None)
        self.page = kwargs.pop('page', None)
        # Get the job application for this session. It could be None.
        self.proposta = get_obj_from_hash(session_hash)
        # Attach the request to "self" so "form_valid()" can access it below.
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print("FORM VALID")
        # This data is valid, so set this form's session hash in the session.
        self.request.session["session_hash"] = form.instance.session_hash
        #current_stage = form.cleaned_data.get("stage")
        current_stage = self._get_stage()

        # Get the next stage after this one.

        new_stage = constants.STAGE_ORDER[
            constants.STAGE_ORDER.index(current_stage) + 1
        ]
        form.instance.stage = new_stage
        form.save()  # This will save the underlying instance.
        if new_stage == constants.COMPLETE:
            return redirect(reverse("delta:obrigado"))
        # else
        return redirect(reverse("delta:proposta", args=(new_stage,)))

    def get_form_class(self):
        print("get_form_class")
        # If we found a job application that matches the session hash, look at
        # its "stage" attribute to decide which stage of the application we're
        # on. Otherwise assume we're on stage 1.
        if self.page:
            stage = self.page
        elif self.proposta:
            stage = self.proposta.stage
        else:
            stage = constants.STAGE_1

        #stage = self.proposta.stage if self.proposta else constants.STAGE_1
        # Get the form fields appropriate to that stage.

        fields = Proposta.get_fields_by_stage(stage)
        # Use those fields to dynamically create a form with "modelform_factory"

        return modelform_factory(Proposta, BaseApplicationForm, fields)

    def get_form_kwargs(self):
        # Make sure Django uses the same JobApplication instance we've already been
        # working on. Otherwise it will instantiate a new one after every submit.
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.proposta
        return kwargs


proposta_view = PropostaView.as_view()


class ObrigadoView(TemplateView):
    template_name = "delta/proposta/obrigado.html"


obrigado_view = ObrigadoView.as_view()
