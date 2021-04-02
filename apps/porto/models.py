import hashlib
import random
import sys
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from .constants import CAMBIO
from .constants import COMBUSTIVEL
from .constants import PRAZO
from .constants import PROFISSAO_ASSALARIADO
from .constants import PROFISSAO_LIBERAL
from .constants import SIMULACAO_INICIAL
from .constants import STAGE_1
from .constants import STAGE_2
from .constants import STAGE_3
from .constants import STAGE_4
from .constants import STAGE_5
from .constants import STAGE_6
from .constants import STATUS
from .constants import STATUS_EM_DIGITACAO
from .constants import STATUS_ERRO
from .constants import STATUS_NAO_SIMULADO
from .constants import STATUS_PRE_RECUSADO
from .constants import STATUS_SIMULACAO
from .constants import TIPO_RENDA
from .constants import UFS
from apps.delta.helpers import model_to_dict_verbose
from apps.users.models import User


def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0, sys.maxsize)).encode("utf-8"))
    return hash.hexdigest()


class PropostaPorto(models.Model):
    FIELDS = {
        STAGE_1: ["valor_do_veiculo", "valor_de_entrada", "valor_financiado", "cpf"],
        STAGE_2: ["prazo"],
        STAGE_3: [
            "nome",
            "data_de_nascimento",
            "sexo",
            "numero_do_rg",
            "orgao_expedidor",
            "nome_da_mae",
            "local_de_nascimento",
            "uf_de_nascimento",
        ],
        STAGE_4: [
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "telefone_fixo",
            "celular",
            "email",
        ],
        STAGE_5: [
            "tipo_de_renda",
            "renda_mensal_pessoal",
            "cep_da_empresa",
            "endereco_comercial",
            "numero_empresa",
            "complemento_empresa",
            "bairro_empresa",
            "cidade_empresa",
            "uf_empresa",
            "inicio_da_atividade",
            "telefone_fixo_da_empresa",
            "tempo_de_empresa",
            "razao_social_da_empresa",
            "cnpj_da_empresa",
            "profissao_liberal",
            "profissao_assalariado",
            "tempo_de_atividade",
            "tempo_de_aposentadoria",
            "outras_rendas",
        ],
        STAGE_6: [
            "ano_de_fabricacao",
            "ano_do_modelo",
            "marca",
            "modelo",
            "versao",
            "combustivel",
            "cambio",
            "motor",
            "cor",
            "dados_placa",
            "placa",
            "renavam",
            "chassi",
        ],
    }

    # operational fields
    user = models.ForeignKey(
        User, null=True, blank=True, verbose_name="Usuário", on_delete=models.SET_NULL
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    simulado_em = models.DateTimeField(null=True, blank=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    modificado_em = models.DateTimeField(auto_now=True)
    session_hash = models.CharField("Código Interno", max_length=40, unique=True)
    pagina = models.PositiveSmallIntegerField("Página", default=1)
    status = models.PositiveSmallIntegerField(
        "Status", choices=STATUS, default=STATUS_NAO_SIMULADO
    )
    estado_simulacao = models.PositiveSmallIntegerField(
        "Simulacao", choices=STATUS_SIMULACAO, default=SIMULACAO_INICIAL
    )
    mensagem = models.CharField(max_length=500, null=True, blank=True)
    valores_parcelas = models.CharField(
        "Valores das parcelas", max_length=1000, null=True, blank=True
    )
    pre_aprovado = models.CharField(
        "Crédito pre-aprovado", max_length=1000, null=True, blank=True
    )

    # stage 1 fields
    valor_do_veiculo = models.CharField(
        "Valor do Veículo",
        max_length=20,
        blank=True,
        help_text="<h2>Veículo</h2><h3>Preencha os dados do financiamento</h3>",
    )
    valor_de_entrada = models.CharField("Valor de Entrada", max_length=20, blank=True)
    valor_financiado = models.CharField("Valor Financiado", max_length=20, blank=True)
    cpf = models.CharField(
        "CPF",
        max_length=20,
        blank=True,
        help_text="<h2>Cliente</h2><h3>Preencha com o CPF do seu Cliente</h3>",
    )

    # stage 2 fields
    prazo = models.CharField(
        "Cotação de Financiamento",
        max_length=3,
        choices=PRAZO,
        blank=False,
        help_text="Selecione a melhor opção para seu cliente.",
       
    )

    # stage 3 fields
    nome = models.CharField("Nome", max_length=100, blank=True)
    data_de_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)
    
    sexo = models.CharField(
        "Sexo",
        max_length=100,
        blank=True,
        choices=(("Masculino", "Masculino"), ("Feminino", "Feminino")),
    )
    numero_do_rg = models.CharField("Número do RG", max_length=100, blank=True)
    orgao_expedidor = models.CharField("Órgão Expedidor", max_length=100, blank=True)
    nome_da_mae = models.CharField("Nome da Mãe", max_length=100, blank=True)
    local_de_nascimento = models.CharField(
        "Local de Nascimento", max_length=100, blank=True
    )
    uf_de_nascimento = models.CharField(
        "UF de Nascimento", max_length=2, choices=UFS, blank=True
    )

    # stage 4 fields
    cep = models.CharField("CEP", max_length=100, blank=True)
    endereco = models.CharField(
        "Endereço (Rua/Avenida/Alameda)", max_length=100, blank=True
    )
    numero = models.CharField("Número", max_length=100, blank=True)
    complemento = models.CharField("Complemento", max_length=100, blank=True)
    bairro = models.CharField("Bairro", max_length=100, blank=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True)
    uf = models.CharField("UF", max_length=2, choices=UFS, blank=True)
    telefone_fixo = models.CharField("Telefone Fixo", max_length=100, blank=True)
    celular = models.CharField("Celular", max_length=100, blank=True)
    email = models.CharField("Email", max_length=100, blank=True)

    # stage 5 fields
    tipo_de_renda = models.CharField(
        # "Tipo de Renda",
        choices=TIPO_RENDA,
        max_length=100,
        blank=True,
        help_text="<h2>Informe a renda do seu cliente</h2>"
        "<h3>Essas informações são essenciais para análise de crédito do "
        "financiamento</h3>"
        "<h3>Tipo de Renda</h3>",
    )
    renda_mensal_pessoal = models.CharField(
        "Renda Mensal Pessoal", max_length=100, blank=True
    )
    profissao_assalariado = models.CharField(
        "Profissão", choices=PROFISSAO_ASSALARIADO, max_length=100, blank=True
    )
    profissao_liberal = models.CharField(
        "Profissão", choices=PROFISSAO_LIBERAL, max_length=100, blank=True
    )
    cep_da_empresa = models.CharField("CEP da Empresa", max_length=100, blank=True)
    endereco_comercial = models.CharField(
        "Endereço Comercial", max_length=100, blank=True
    )
    numero_empresa = models.CharField("Número", max_length=100, blank=True)
    complemento_empresa = models.CharField("Complemento", max_length=100, blank=True)
    bairro_empresa = models.CharField("Bairro", max_length=100, blank=True)
    cidade_empresa = models.CharField("Cidade", max_length=100, blank=True)
    uf_empresa = models.CharField("UF", max_length=2, choices=UFS, blank=True)
    inicio_da_atividade = models.DateField("Início da Atividade", blank=True, null=True)
    telefone_fixo_da_empresa = models.CharField(
        "Telefone Fixo da Empresa", max_length=100, blank=True
    )
    tempo_de_empresa = models.CharField(
        "Tempo de Empresa (anos)", max_length=100, blank=True
    )
    razao_social_da_empresa = models.CharField(
        "Razão Social da Empresa", max_length=100, blank=True
    )
    cnpj_da_empresa = models.CharField("CNPJ da empresa", max_length=100, blank=True)
    # profissao = models.CharField(max_length=100, blank=True)
    tempo_de_atividade = models.CharField(
        "Tempo de Atividade", max_length=100, blank=True
    )
    tempo_de_aposentadoria = models.CharField(
        "Tempo de Aposentadoria", max_length=100, blank=True
    )
    outras_rendas = models.CharField("Outras Rendas", max_length=100, blank=True)

    # stage 6 fields
    ano_de_fabricacao = models.CharField(
        "Ano de Fabricação",
        max_length=100,
        blank=True,
        help_text="<h2>Informações sobre o Veículo</h2><p>Caso seu cliente não saiba "
        "extamente qual veículo irá comprar, indique algum compatível em "
        "termos de preço. Fique tranquilo, você poderá mudar essa informação "
        "a qualquer momento.</p>",
    )
    ano_do_modelo = models.CharField("Ano do Modelo", max_length=100, blank=True)
    marca = models.CharField("Marca", max_length=100, blank=True)
    modelo = models.CharField("Modelo", max_length=100, blank=True)
    versao = models.CharField("Versão", max_length=100, blank=True)
    cor = models.CharField("Cor", max_length=100, blank=True)
    combustivel = models.CharField(
        "Combustível", choices=COMBUSTIVEL, max_length=100, blank=True
    )
    cambio = models.CharField("Câmbio", choices=CAMBIO, max_length=100, blank=True)
    motor = models.CharField("Motor", max_length=100, blank=True)
    dados_placa = models.CharField(
        "VOCÊ POSSUI OS DADOS DE PLACA / CHASSI / RENAVAM DESTE VEÍCULO?",
        choices=(("Sim", "Sim"), ("Não", "Não")),
        max_length=100,
        blank=True,
    )

    placa = models.CharField("Placa", max_length=100, blank=True)
    renavam = models.CharField("Renavam", max_length=100, blank=True)
    chassi = models.CharField("Chassi", max_length=100, blank=True)

    nome_operador = models.CharField("Nome do Operador", max_length=100, blank=True)

    # Config
    # hidden_fields = ["stage", "session_hash", "operador"]
    hidden_fields = ["pagina", "session_hash", "nome_operador"]
    radio_fields = ["prazo", "sexo", "tipo_de_renda", "dados_placa"]
    readonly_fields = ["valor_financiado"]

    required_fields = [
        "valor_do_veiculo",
        "valor_de_entrada",
        "cpf",
        "prazo",
        "nome",
        "data_de_nascimento",
        "sexo",
        "numero_do_rg",
        "orgao_expedidor",
        "nome_da_mae",
        "local_de_nascimento",
        "uf_de_nascimento",
        "cep",
        "endereco",
        "numero",
        # 'complemento',
        "bairro",
        "cidade",
        "uf",
        # 'telefone_fixo',
        "celular",
        "email",
        "tipo_de_renda",
        "renda_mensal_pessoal",
        # "profissao",
        # "cep_da_empresa",
        # "endereco_comercial",
        # "numero_empresa",
        # # 'complemento_empresa',
        # "bairro_empresa",
        # "cidade_empresa",
        # "uf_empresa",
        # "inicio_da_atividade",
        # "telefone_fixo_da_empresa",
        # "tempo_de_empresa",
        # "razao_social_da_empresa",
        # "cnpj_da_empresa",
        # "tempo_de_atividade",
        # "tempo_de_aposentadoria",
        # "outras_rendas",
        "ano_de_fabricacao",
        "ano_do_modelo",
        "marca",
        "modelo",
        "versao",
        "combustivel",
        "cambio",
        "motor",
        # 'placa',
        # 'renavam',
        # 'chassi'
    ]

    class Meta:
        verbose_name = "Proposta Porto Seguro"
        verbose_name_plural = "Propostas Porto Seguro"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_hash()

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

    def to_numeric(self, value):
        n = (
            value.strip()
            .replace("R", "")
            .replace("$", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", ".")
        )
        return Decimal(n)

    @property
    def numero_valor_do_veiculo(self):
        return self.to_numeric(self.valor_do_veiculo)

    @property
    def numero_valor_de_entrada(self):
        return self.to_numeric(self.valor_de_entrada)

    def get_veiculo(self):
        veiculo = [
            self.marca,
            self.modelo,
            self.versao,
            self.ano_de_fabricacao,
            self.ano_do_modelo,
            self.cor,
            self.motor,
            self.cambio,
        ]
        return " ".join(filter(None, veiculo))

    def simular(self):
        from .tasks import run_simulation

        # get_simulation(self.pk)
        self.status = STATUS_NAO_SIMULADO
        self.save()
        run_simulation.delay(self.pk)
        # if settings.DEBUG:
        #    get_simulation(self.pk)
        # else:
        #    get_simulation.delay(self.pk)

    def salvar_simulacao(self, valores_parcelas, pre_aprovado):
        self.valores_parcelas = valores_parcelas
        self.pre_aprovado = pre_aprovado
        self.simulado_em = timezone.now()
        self.status = STATUS_EM_DIGITACAO
        self.save()

    def recusar(self,):
        self.simulado_em = timezone.now()
        self.status = STATUS_PRE_RECUSADO
        self.save()

    def erro(self,):
        self.simulado_em = timezone.now()
        self.status = STATUS_ERRO
        self.save()

    @property
    def time_simulated(self):
        if self.criado_em and self.simulado_em:
            return self.simulado_em.replace(microsecond=0) - self.criado_em.replace(
                microsecond=0
            )

    @property
    def time_total(self):
        if self.enviado_em and self.simulado_em:
            return self.enviado_em.replace(microsecond=0) - self.criado_em.replace(
                microsecond=0
            )

    def create_hash(self):
        if not self.session_hash:
            while True:
                session_hash = create_session_hash()
                if PropostaPorto.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    @staticmethod
    def get_fields_by_stage(stage):
        fields = ["pagina"]  # Must always be present
        fields.extend(PropostaPorto.FIELDS[stage])
        return fields

    def save(self, *args, **kwargs):

        super(PropostaPorto, self).save(*args, **kwargs)

    def get_to_email(self):
        if self.user:
            email = self.user.get_email()
            if email:
                return email
        return settings.DEFAULT_TO_EMAIL

    def finish(self):
        from apps.gestao.models import Proposta

        self.send_mail()
        Proposta.create_from_porto(self)

    def send_mail(self):
        from apps.delta.tasks import send_default_email

        self.enviado_em = timezone.now()
        self.save()

        dic = model_to_dict_verbose(self, exclude=["id"] + self.hidden_fields)

        to_email = self.get_to_email()
        send_default_email.delay(dic, "Proposta", to_email)

    @property
    def loja(self):
        return self.user.loja
