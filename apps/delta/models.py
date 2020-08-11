# Create your models here.
import hashlib
import random
import sys

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from . import constants
from .helpers import model_to_dict_verbose
from apps.users.models import User


def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0, sys.maxsize)).encode("utf-8"))
    return hash.hexdigest()


class Proposta(models.Model):
    FIELDS = {
        constants.STAGE_1: [
            "valor_do_veiculo",
            "valor_de_entrada",
            "cpf",
            "nome_operador",
        ],
        constants.STAGE_2: ["prazo"],
        constants.STAGE_3: [
            "nome",
            "data_de_nascimento",
            "sexo",
            "numero_do_rg",
            "orgao_expedidor",
            "nome_da_mae",
            "local_de_nascimento",
            "uf_de_nascimento",
        ],
        constants.STAGE_4: [
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
        constants.STAGE_5: [
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
        constants.STAGE_6: [
            "ano_de_fabricacao",
            "ano_do_modelo",
            "marca",
            "modelo",
            "versao",
            "combustivel",
            "cambio",
            "motor",
            "dados_placa",
            "placa",
            "renavam",
            "chassi",
        ],
    }
    PRAZO = (("12", "12x"), ("24", "24x"), ("36", "36x"), ("48", "48x"), ("60", "60x"))

    UFS = [
        ("AC", "AC"),
        ("AL", "AL"),
        ("AP", "AP"),
        ("AM", "AM"),
        ("BA", "BA"),
        ("CE", "CE"),
        ("DF", "DF"),
        ("ES", "ES"),
        ("GO", "GO"),
        ("MA", "MA"),
        ("MT", "MT"),
        ("MS", "MS"),
        ("MG", "MG"),
        ("PA", "PA"),
        ("PB", "PB"),
        ("PR", "PR"),
        ("PE", "PE"),
        ("PI", "PI"),
        ("RJ", "RJ"),
        ("RN", "RN"),
        ("RS", "RS"),
        ("RO", "RO"),
        ("RR", "RR"),
        ("SC", "SC"),
        ("SP", "SP"),
        ("SE", "SE"),
        ("TO", "TO"),
    ]

    TIPO_RENDA2 = [
        ("assalariado", "Assalariado"),
        ("autonomo", "Profissional liberal/Autônomo"),
        ("empresario", "Empresário"),
        ("aposentado", "Aposentado"),
    ]

    TIPO_RENDA = [
        ("assalariado", "assalariado"),
        ("autonomo", "autonomo"),
        ("empresario", "empresario"),
        ("aposentado", "aposentado"),
    ]

    PROFISSAO_ASSALARIADO = [
        ("ADMINISTRADORES / ECONOMISTAS", "ADMINISTRADORES / ECONOMISTAS"),
        ("ANALISTAS", "ANALISTAS"),
        ("CONSULTOR", "CONSULTOR"),
        ("DIRETOR DE EMPRESA", "DIRETOR DE EMPRESA"),
        ("FUNCIONÁRIO DE EMPRESAS PUBLICAS", "FUNCIONÁRIO DE EMPRESAS PUBLICAS"),
        ("GERENTE", "GERENTE"),
        ("OPERADOR EM GERAL", "OPERADOR EM GERAL"),
        ("OUTRAS PROFISSÕES DA INDUSTRIA", "OUTRAS PROFISSÕES DA INDUSTRIA"),
        ("OUTRAS PROFISSÕES NO COMÉRCIO", "OUTRAS PROFISSÕES NO COMÉRCIO"),
        ("PROFESSORES", "PROFESSORES"),
        ("PROMOTOR", "PROMOTOR"),
        (
            "VENDEDORES / REPRESENTANTES / INTERMEDIÁRIOS",
            "VENDEDORES / REPRESENTANTES / INTERMEDIÁRIOS",
        ),
        ("OUTROS", "OUTROS"),
    ]

    PROFISSAO_LIBERAL = [
        ("ADVOGADOS", "ADVOGADOS"),
        ("ARQUITETOS", "ARQUITETOS"),
        ("ENGENHEIROS", "ENGENHEIROS"),
        ("MÉDICOS E CIRURGIÕES DENTISTAS", "MÉDICOS E CIRURGIÕES DENTISTAS"),
        ("PROFESSORES", "PROFESSORES"),
        ("OUTROS", "OUTROS"),
    ]

    # operational fields
    criado_em = models.DateTimeField(auto_now_add=True)
    simulado_em = models.DateTimeField(null=True, blank=True)
    enviado_em = models.DateTimeField(null=True, blank=True)
    modificado_em = models.DateTimeField(auto_now=True)
    session_hash = models.CharField("Código Interno", max_length=40, unique=True)
    stage = models.CharField("Estágio", max_length=10, default="1")
    valores_parcelas = models.CharField(
        "Valores das parcelas", max_length=1000, null=True, blank=True
    )

    # stage 1 fields
    valor_do_veiculo = models.CharField(
        "Valor do Veículo",
        max_length=20,
        blank=True,
        help_text="<h2>Veículo</h2><h3>Preencha os dados do financiamento</h3>",
    )
    valor_de_entrada = models.CharField("Valor de Entrada", max_length=20, blank=True)
    cpf = models.CharField(
        "CPF",
        max_length=20,
        blank=True,
        help_text="<h2>Cliente</h2><h3>Preencha com o CPF do seu Cliente</h3>",
    )

    # stage 2 fields
    prazo = models.CharField("Prazo", max_length=3, choices=PRAZO, blank=False)

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
        "Tipo de Renda",
        choices=TIPO_RENDA,
        max_length=100,
        blank=True,
        help_text="<h2>Informe a renda do seu cliente</h2>"
        "<h3>Essas informações são essenciais para análise de crédito do "
        "financiamento</h3>",
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
    inicio_da_atividade = models.CharField(
        "Início da Atividade", max_length=100, blank=True
    )
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
        "Ano de Fabricação", max_length=100, blank=True, help_text="Veículo"
    )
    ano_do_modelo = models.CharField("Ano do Modelo", max_length=100, blank=True)
    marca = models.CharField("Marca", max_length=100, blank=True)
    modelo = models.CharField("Modelo", max_length=100, blank=True)
    versao = models.CharField("Versão", max_length=100, blank=True)
    combustivel = models.CharField("Combustível", max_length=100, blank=True)
    cambio = models.CharField("Câmbio", max_length=100, blank=True)
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
    hidden_fields = ["stage", "session_hash", "nome_operador"]
    radio_fields = ["prazo", "sexo", "tipo_de_renda", "dados_placa"]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_hash()
        # print([n.name for n in self._meta.fields])

    def __str__(self):
        return f"{self.nome} - {self.cpf}"

    def salvar_simulacao(self, valores_parcelas):
        self.valores_parcelas = valores_parcelas
        self.simulado_em = timezone.now()
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
                if Proposta.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    @staticmethod
    def get_fields_by_stage(stage):
        fields = ["stage"]  # Must always be present
        fields.extend(Proposta.FIELDS[stage])
        return fields

    def save(self, *args, **kwargs):
        super(Proposta, self).save(*args, **kwargs)

    def get_to_email(self):
        user = User.objects.filter(username=self.nome_operador).first()
        if user:
            return user.email
        return settings.DEFAULT_TO_EMAIL

    def send_mail(self):
        from .tasks import send_default_email

        self.enviado_em = timezone.now()
        self.save()

        dic = model_to_dict_verbose(self, exclude=["id"] + self.hidden_fields)

        to_email = self.get_to_email()
        send_default_email.delay(dic, "Proposta", to_email)


class FinanciamentoVeiculo(models.Model):
    valor_do_veiculo = models.CharField("Valor do Veículo", max_length=100)
    entrada = models.CharField("Valor de Entrada", max_length=100)
    cpf = models.CharField("CPF", max_length=100)
    telefone = models.CharField("Telefone", max_length=100)

    class Meta:
        verbose_name = "Financiamento de Veículo"
        verbose_name_plural = "Financiamentos de Veículos"

    def __str__(self):
        return f"Financiamento de Veículo: {self.cpf} - {self.valor_do_veiculo}"


class CartaoCredito(models.Model):
    OPCOES_PESSOA = (("fisica", "Pessoa Física"), ("juridica", "Pessoa Jurídica"))
    OPCOES_BANDEIRA = (("visa", "Visa"), ("master", "Master"))
    OPCOES_SEXO = (("masculino", "Masculino"), ("feminino", "Feminino"))
    OPCOES_VENCIMENTO = (
        ("1", "1"),
        ("5", "5"),
        ("10", "10"),
        ("15", "15"),
        ("20", "20"),
        ("25", "25"),
        ("30", "30"),
    )

    nome = models.CharField("Nome completo", max_length=254)
    email = models.EmailField("E-mail")
    telefone = models.CharField("Telefone", max_length=50)
    cpf = models.CharField("CPF", max_length=100)
    pessoa = models.CharField("Pessoa", choices=OPCOES_PESSOA, max_length=100)
    bandeira = models.CharField("Bandeira", choices=OPCOES_BANDEIRA, max_length=100)
    sexo = models.CharField("Sexo", choices=OPCOES_SEXO, max_length=100)
    data_de_nascimento = models.DateField("Data de Nascimento")
    nome_mae = models.CharField("Nome da mãe", max_length=254)
    endereco = models.CharField("Endereço Residencial", max_length=254)
    cep = models.CharField("CEP", max_length=12)
    vencimento = models.CharField(
        "Dia do Vencimento", choices=OPCOES_VENCIMENTO, max_length=2
    )

    # Config
    radio_fields = ["pessoa", "bandeira", "sexo", "vencimento"]

    class Meta:
        verbose_name = "Cartão de Crédito"
        verbose_name_plural = "Cartões de Crédito"

    def __str__(self):
        return f"Cartão de Crédito: {self.cpf}"


class CapitalGiro(models.Model):
    OPCOES_FATURAMENTO = (
        ("200-500", "200 mil - 500 mil"),
        ("500-1", "500 mil - 1 milhão"),
        ("1-2", "1 milhão - 2 milhões"),
        ("2-5", "2 milhões - 5 milhões"),
        ("5-10", "5 milhões - 10 milhões"),
        ("10-20", "10 milhões - 20 milhões"),
        ("20-30", "20 milhões - 30 milhões"),
        ("30-50", "30 milhões - 50 milhões"),
        ("50-", "acima de 50 milhões"),
    )

    nome = models.CharField("Nome completo", max_length=300)
    email = models.EmailField("E-mail")
    telefone = models.CharField("Telefone", max_length=300)
    prazo = models.PositiveSmallIntegerField(
        "Prazo", validators=[MaxValueValidator(24)], help_text="1x a 24x"
    )
    cnpj = models.CharField("CNPJ", max_length=100)
    faturamento_anual = models.CharField(
        "Faturamento anual da empresa", choices=OPCOES_FATURAMENTO, max_length=100
    )
    valor_emprestimo = models.CharField(
        "Valor do emprestimo", max_length=100, help_text="Máximo de 800 mil"
    )

    class Meta:
        verbose_name = "Capital de Giro"
        verbose_name_plural = "Capitais de Giro"
