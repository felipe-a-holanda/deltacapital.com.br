import decimal
import time
from decimal import Decimal

from celery.utils.log import get_task_logger
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from splinter import Browser

from .constants import STATUS_EM_DIGITACAO
from .constants import STATUS_ERRO
from .constants import STATUS_PRE_RECUSADO
from .models import PropostaPorto
from config import celery_app


logger = get_task_logger(__name__)


HEADLESS = True




PORTO_URL = "https://financeiraportoseguro.com.br/auto/?usrtip=S12345&webusrcod=108558&portal=2"

SUSEP = "3B501J"

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
    browser = Browser("chrome", headless=HEADLESS, executable_path=settings.CHROMEDRIVER_PATH)
    return browser



def porto_page_0(browser, data):
    time.sleep(1)
    browser.fill("SUSEP", SUSEP)
    browser.find_by_text("Continuar").last.click()

def porto_page_1(browser, data):
    data = adapt_data(data)
    time.sleep(4)
    browser.fill("Valor", data["Valor"])
    browser.fill("EntradaOutro", data["EntradaOutro"])
    for key in browser.type("CPF", data["CPF"], slowly=True):
        pass
    slider = browser.find_by_css("span.ui-slider-handle")
    for i in range(10):
        slider.type(Keys.RIGHT)
        time.sleep(0.2)

    browser.find_by_text("Ver parcelas").last.click()


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


def find_parcelas(browser):
    parcelas_c = [
        browser.find_by_css("#parcelas-c-%d > label" % i).text for i in range(5)
    ]
    parcelas_1 = [
        browser.find_by_css("#parcelas-%d > label" % i).text for i in range(5)
    ]
    if parcelas_1[0]:
        parcelas = parcelas_1
    else:
        parcelas = parcelas_c
    logger.info(parcelas)
    return parcelas


def porto_page_2(browser, data):
    is_aprovado = browser.is_element_present_by_id("prestamista", wait_time=30)
    if is_aprovado:
        prestamista = browser.find_by_css("span.ps-frm-onOff-switch").first
        prestamista.click()
        time.sleep(4)
        browser.is_element_present_by_name("Parcelas", wait_time=30)

        valores = find_parcelas(browser)

        pre_aprovado_box = browser.find_by_css(".valor-aprovado-box").first
        pre_aprovado = browser.find_by_css(".valor-aprovado").first

        valor_pre_aprovado = clean_currency(pre_aprovado.text)

        if valor_pre_aprovado > 0:
            print("Proposta aprovada com valor pre aprovado")
            return STATUS_EM_DIGITACAO, valores, pre_aprovado_box.text
        else:
            print("Proposta aprovada")
            return STATUS_EM_DIGITACAO, valores, ""
    else:
        header = browser.find_by_css(".title-widget").first.text
        if "pelo interesse" in header:
            print("Proposta RECUSADA")
            return STATUS_PRE_RECUSADO, None, None

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

    porto_page_0(browser, data)

    porto_page_1(browser, data)

    status, valores_parcelas, pre_aprovado = porto_page_2(browser, data)

    proposta = PropostaPorto.objects.get(pk=pk)

    if status == STATUS_EM_DIGITACAO:
        proposta.salvar_simulacao(valores_parcelas, pre_aprovado)
        return valores_parcelas, pre_aprovado
    elif status == STATUS_PRE_RECUSADO:
        proposta.recusar()
    else:
        proposta.erro()

    return False
