from django import forms
from django.conf import settings
from json2html import json2html

from .shiftdata_api import ShiftData

SHIFTDATA_API_KEY = settings.SHIFTDATA_API_KEY
SHIFTDATA_BASE_URL = "https://api.shiftdata.com.br"


class ShiftDataForm(forms.Form):
    cpf = forms.CharField(help_text="Somente números", max_length=11)

    def call_api(self):
        api = ShiftData(SHIFTDATA_BASE_URL, SHIFTDATA_API_KEY)
        cpf = self.cleaned_data["cpf"]
        result = api.pessoa_fisica(cpf)
        if result["code"] == 200:
            return json2html.convert(result["result"])
        return result["message"]
