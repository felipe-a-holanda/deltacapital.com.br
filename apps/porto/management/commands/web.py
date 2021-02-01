from django.core.management.base import BaseCommand
from apps.porto.web import SeleniumBrowsing


from ...constants import Valores
class Command(BaseCommand):
    help = 'Run browswr'



    def handle(self, *args, **options):
        values = {
            "valor":"10000000",
            "entrada":"3000000",
            #"cpf":"82721351320",
            "cpf":"01614475385",
        }
        valores = Valores("10000000", "3000000", "01614475385")


        SeleniumBrowsing().run(valores)