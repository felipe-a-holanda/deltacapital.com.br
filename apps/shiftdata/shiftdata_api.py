from urllib.parse import urljoin

import requests


SHIFTDATA_API_KEY = ""
SHIFTDATA_BASE_URL = "https://api.shiftdata.com.br"


class ShiftData(object):
    """
    https://api.shiftdata.com.br/swagger/index.html
    """

    def __init__(self, base_url=SHIFTDATA_BASE_URL, api_key=SHIFTDATA_API_KEY):
        self.api_key = api_key
        self.base_url = base_url
        self.token = ""
        self.login()

    def request_post(self, endpoint, data=None, json=None):
        url = urljoin(self.base_url, endpoint)
        response = requests.post(url, data, json)
        return response.json()

    def request_get(self, endpoint, params):
        url = urljoin(self.base_url, endpoint)
        headers = {"authorization": "Bearer " + self.token}
        response = requests.get(url, params, headers=headers)
        return response.json()

    def login(self):
        endpoint = "/api/Login"
        url = urljoin(self.base_url, endpoint)
        parameters = {"accessKey": self.api_key}
        response = requests.post(url, json=parameters)
        if response.status_code == 200:
            data = response.json()
            self.token = data["accessToken"]
            self.expiration = data["expiration"]

            return True

    def pessoa_fisica(self, cpf):
        endpoint = "/api/PessoaFisica"
        return self.request_get(endpoint, params={"cpf": cpf})

    def pessoa_juridica(self, cnpj):
        endpoint = "/api/PessoaJuridica"
        return self.request_get(endpoint, params={"cnpj": cnpj})

    def vinculos_empresariais(self, cpf):
        endpoint = "/api/VinculosEmpresariais"
        return self.request_get(endpoint, params={"cpf": cpf})

    def participacao_empresarial(self, cpf):
        endpoint = "/api/ParticipacaoEmpresarial"
        return self.request_get(endpoint, params={"cpf": cpf})


if __name__ == "__main__":
    api = ShiftData()
