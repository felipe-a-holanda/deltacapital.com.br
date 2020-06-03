# Create your views here.
from urllib.parse import quote
from django.http import Http404
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.template import TemplateDoesNotExist
from constance import config

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