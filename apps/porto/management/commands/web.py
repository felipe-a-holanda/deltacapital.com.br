from django.core.management.base import BaseCommand

from ...constants import Valores
from apps.porto.web import SeleniumBrowsing


class Command(BaseCommand):
    help = "Run browswr"

    def handle(self, *args, **options):
        valores = Valores("10000000", "3000000", "01614475385")

        SeleniumBrowsing().run(valores)
