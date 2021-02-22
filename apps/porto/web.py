import decimal
import logging
import time
from decimal import Decimal

import selenium
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .constants import ResultadoSimulacao
from .constants import SIMULACAO_APROVADO
from .constants import SIMULACAO_ERRO
from .constants import SIMULACAO_INICIAL
from .constants import SIMULACAO_RECUSADO


GOOGLE_CHROME_PATH = settings.GOOGLE_CHROME_PATH
CHROMEDRIVER_PATH = settings.CHROMEDRIVER_PATH

URL = "https://financeiraportoseguro.com.br/auto/?webusrcod=108558&portal=2"
SUSEP = "3B501J"

logger = logging.getLogger(__name__)


def format_currency(d):
    return "{0:.2f}".format(d).replace(".", "")


def clean_currency(text):
    new_text = (
        text.replace("R", "")
        .replace("$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )
    print("Converting:", text, new_text)
    try:
        d = Decimal(new_text)
    except decimal.InvalidOperation:
        d = Decimal(0)
        logger.info("Erro no decimal: " + new_text)
    return d


class SeleniumBrowsing(object):
    def __init__(
        self, chrome_path=GOOGLE_CHROME_PATH, driver_path=CHROMEDRIVER_PATH, url=URL
    ):
        self.chrome_path = chrome_path
        self.driver_path = driver_path
        self.url = url

        self.state = SIMULACAO_INICIAL
        self.parcelas = None
        self.mensagem = None
        self.pre_aprovado = None

    def run(self, pk):
        from apps.porto.models import PropostaPorto

        self.model = PropostaPorto.objects.get(pk=pk)
        values = self.get_values_from_model(self.model)
        try:
            self.simulate(values)
        except selenium.common.exceptions.TimeoutException:
            self.set_status_erro()

    def set_estatus(self, status):
        self.model.estado_simulacao = status
        self.model.save()

    def set_status_erro(self):
        self.set_estatus(SIMULACAO_ERRO)

    def get_values_from_model(self, model):
        valor = format_currency(model.numero_valor_do_veiculo)
        entrada = format_currency(model.numero_valor_de_entrada)

        data = dict(valor=valor, entrada=entrada, cpf=model.cpf)
        return data

    def simulate(self, values):

        logger.info("Iniciando Simulacao")
        self.start()
        logger.info("Pagina 1 Susep")
        self.page_1()
        logger.info("Pagina 2 Valores")
        self.page_2(values)
        logger.info("Pagina 2 Parcelas")
        self.page_3()

        resultado = ResultadoSimulacao(self.state, self.parcelas, self.mensagem)

        self.model.valores_parcelas = self.parcelas
        self.model.mensagem = self.mensagem
        self.model.pre_aprovado = self.pre_aprovado
        self.model.estado_simulacao = self.state
        self.model.save()

        print(resultado)
        return resultado

    def start(self):
        chrome_options = webdriver.ChromeOptions()
        # .headless = True
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = self.chrome_path
        driver = webdriver.Chrome(
            executable_path=self.driver_path, chrome_options=chrome_options
        )
        self.driver = driver
        return driver

    def page_1(self):
        self.driver.get(self.url)
        susep = self.driver.find_element_by_name("SUSEP")
        self.slow_type(susep, SUSEP)

        button = self.driver.find_element_by_css_selector("#verificarSusep button")
        button.click()

    def page_2(self, values):
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "susepInfo"), "DELTA")
        )

        element_valor = self.driver.find_element_by_name("Valor")
        element_entrada = self.driver.find_element_by_name("EntradaOutro")
        element_cpf = self.driver.find_element_by_name("CPF")

        valor = values["valor"]
        entrada = values["entrada"]
        cpf = values["cpf"]

        self.slow_type(element_valor, valor)
        self.slow_type(element_entrada, entrada)
        self.slow_type(element_cpf, cpf)

        slider = self.driver.find_element_by_css_selector("span.ui-slider-handle")
        for i in range(10):
            slider.send_keys(Keys.ARROW_RIGHT)
            time.sleep(0.2)

        self.driver.find_element_by_xpath("//*[text()='Ver parcelas']").click()

    def page_3(self):

        element = WebDriverWait(self.driver, 10).until(
            lambda driver: driver.find_elements_by_id("prestamista")
            or driver.find_elements_by_xpath("//*[text()[contains(., 'interesse')]]")
        )[0]
        logger.info(f"element={element}")

        if "interesse" in element.text:
            self.state = SIMULACAO_RECUSADO
            self.mensagem = element.text
            return

        self.driver.execute_script("arguments[0].click();", element)
        self.driver.implicitly_wait(1)

        parcelas_prestamista = self._get_parcelas()
        try:
            element = WebDriverWait(self.driver, 10).until(
                lambda driver: self._get_parcelas()
                and self._get_parcelas() != parcelas_prestamista
            )
        except TimeoutException:
            logger.warning("Sem opcao de seguro prestamista")

        self.parcelas = self._get_parcelas()
        self.pre_aprovado = self.get_mensagem_aprovado()
        self.state = SIMULACAO_APROVADO

    def _get_parcelas(self):
        elements_parcelas = self.driver.find_elements_by_css_selector(
            "input[name='Parcelas']"
        )
        parcelas_set = set()
        for p in elements_parcelas:
            x = p.get_attribute("value")
            value = "%.2f" % float(p.get_attribute("alt").split("|")[0])
            parcelas_set.add((x, value))
        parcelas = sorted(list(parcelas_set))
        return parcelas

    def get_mensagem_aprovado(self):
        pre_aprovado_box = self.driver.find_element_by_css_selector(
            ".valor-aprovado-box"
        )
        pre_aprovado = self.driver.find_element_by_css_selector(".valor-aprovado")
        valor_pre_aprovado = clean_currency(pre_aprovado.text)
        message = ""
        if valor_pre_aprovado > 0:
            message = pre_aprovado_box.text

        return message

    def slow_type(self, element, text, delay=0.1):
        """Send a text to an element one character at a time with a delay."""
        for character in text:
            element.send_keys(character)
            time.sleep(delay)


def test_recusa():
    pass


def test_aprovado():
    pass


def test_aprovado_com_limite():
    pass


def do_tests():
    test_recusa()
    test_aprovado()
    test_aprovado_com_limite()


if __name__ == "__main__":
    do_tests()
