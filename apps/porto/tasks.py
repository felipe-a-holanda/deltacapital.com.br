import time
from decimal import Decimal

from celery.utils.log import get_task_logger
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from splinter import Browser

from .constants import STATUS_APROVADO
from .constants import STATUS_ERRO
from .constants import STATUS_RECUSADO
from .models import PropostaPorto
from config import celery_app

logger = get_task_logger(__name__)


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


fields_dic = {
    "valor_do_veiculo": "Valor",
    "valor_de_entrada": "EntradaOutro",
    "cpf": "CPF",
}
numeric_fields = ["valor_do_veiculo", "valor_de_entrada", "cpf"]


def adapt_data(data_dic):
    new_data = {}
    for key, value in data_dic.items():
        if key in numeric_fields:
            value = "".join([c for c in value if c.isdigit()])
        new_key = fields_dic.get(key, key)
        new_data[new_key] = value
    return new_data


def start_selenium_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = settings.GOOGLE_CHROME_PATH
    browser = webdriver.Chrome(
        executable_path=settings.CHROMEDRIVER_PATH, chrome_options=chrome_options
    )
    return browser


def start_splinter_browser():
    # browser = Browser("chrome")
    browser = Browser("chrome", headless=True)
    return browser


def porto_page_1(browser, data):
    data = adapt_data(data)

    browser.fill("Valor", data["Valor"])
    browser.fill("EntradaOutro", data["EntradaOutro"])
    for key in browser.type("CPF", data["CPF"], slowly=True):
        pass
    slider = browser.find_by_css("span.ui-slider-handle")
    for i in range(10):
        slider.type(Keys.RIGHT)
        time.sleep(0.2)

    # browser.find_by_css("button[type='submit']").last.click()
    browser.find_by_css(
        "#propostaCorretor > div:nth-child(9) > div > button"
    ).last.click()


def porto_page_2(browser, data):
    is_aprovado = browser.is_element_present_by_id("prestamista", wait_time=20)
    if is_aprovado:
        prestamista = browser.find_by_css("span.ps-frm-onOff-switch").first
        prestamista.click()
        time.sleep(4)
        browser.is_element_present_by_name("Parcelas", wait_time=20)
        parcelas = [browser.find_by_css("#parcelas-c-%d > label" % i) for i in range(5)]

        valores = [parcela.text for parcela in parcelas]
        # valores = {parcela._element.get_attribute('value'): parcela.text for parcela in parcelas}

        try:
            pre_aprovado = browser.find_by_css(".valor-aprovado-box").first
            print("Proposta aprovada com valor pre aprovado")
            return STATUS_APROVADO, valores, pre_aprovado.text
        except:  # noqa: E722
            print("Proposta aprovada")
            return STATUS_APROVADO, valores, ""
    else:
        header = browser.find_by_css(".title-widget").first.text
        if "pelo interesse" in header:
            print("Proposta RECUSADA")
            return STATUS_RECUSADO, None, None

    print("ERRO NA SIMULACAO")
    return STATUS_ERRO, None, None


def format_currency(m):
    return "{0:.2f}".format(
        Decimal(m.replace("R", "").replace("$", "").replace(",", ""))
    ).replace(".", "")


def data_from_model(pk):
    proposta = PropostaPorto.objects.get(pk=pk)

    valor = format_currency(proposta.valor_do_veiculo)
    entrada = format_currency(proposta.valor_de_entrada)
    data = dict(Valor=valor, EntradaOutro=entrada, CPF=proposta.cpf)
    return data


@celery_app.task
def get_simulation(pk):
    data = data_from_model(pk)

    browser = start_splinter_browser()
    browser.visit(PORTO_URL)

    porto_page_1(browser, data)

    status, valores_parcelas, pre_aprovado = porto_page_2(browser, data)

    proposta = PropostaPorto.objects.get(pk=pk)

    if status == STATUS_APROVADO:
        proposta.salvar_simulacao(valores_parcelas, pre_aprovado)
        return valores_parcelas, pre_aprovado
    elif status == STATUS_RECUSADO:
        proposta.recusar()
    else:
        proposta.erro()

    return False
