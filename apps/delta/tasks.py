import time

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from splinter import Browser

from .models import Proposta
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


@celery_app.task
def send_default_email(object, subject="", to_email=None):

    msg_plain = render_to_string("delta/emails/email.txt", {"object": object})
    msg_html = render_to_string("delta/emails/email.html", {"object": object})

    from_email = settings.DEFAULT_FROM_EMAIL
    if not to_email:
        to_email = settings.DEFAULT_TO_EMAIL
    prefix = settings.EMAIL_SUBJECT_PREFIX

    nome = object.get("Nome", "")

    subject_email = f"{prefix} {subject} {nome}"

    send_mail(subject_email, msg_plain, from_email, [to_email], html_message=msg_html)

    logger.info(f"Email sent [{subject}]")
    logger.info(f"{msg_plain}")
    logger.info(f"{msg_html}")


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
    browser = Browser("chrome")
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
    h2 = [i.text for i in browser.find_by_css("h2")]
    if any(["interesse" in h for h in h2]):
        return None

    browser.is_element_present_by_id("prestamista", wait_time=20)
    prestamista = browser.find_by_css("span.ps-frm-onOff-switch").first
    prestamista.click()
    time.sleep(4)
    browser.is_element_present_by_name("Parcelas", wait_time=20)
    parcelas = [browser.find_by_css("#parcelas-c-%d > label" % i) for i in range(5)]

    valores = [parcela.text for parcela in parcelas]
    # valores = {parcela._element.get_attribute('value'): parcela.text for parcela in parcelas}

    return valores


@celery_app.task
def get_simulation(pk, data):
    data = adapt_data(data)

    browser = start_splinter_browser()
    browser.visit(PORTO_URL)

    porto_page_1(browser, data)

    valores_parcelas = porto_page_2(browser, data)
    if valores_parcelas:
        proposta = Proposta.objects.get(pk=pk)
        proposta.salvar_simulacao(valores_parcelas)
        return valores_parcelas

    return False
