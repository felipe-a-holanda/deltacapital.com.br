from urllib.parse import quote

from constance import config
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CapitalGiroForm
from .forms import CartaoCreditoForm
from .forms import FinanciamentoVeiculoForm
from .helpers import model_to_dict_verbose
from .models import CapitalGiro
from .models import CartaoCredito
from .models import FinanciamentoVeiculo
from .tasks import send_default_email


class HomeView(TemplateView):
    template_name = "delta/index.html"


home_view = HomeView.as_view()


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


class ObrigadoView(TemplateView):
    template_name = "delta/obrigado.html"


obrigado_view = ObrigadoView.as_view()


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
