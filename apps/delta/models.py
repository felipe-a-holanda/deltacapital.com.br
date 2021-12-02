# Create your models here.
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone


class TimedModel(models.Model):
    criado_em = models.DateTimeField(blank=True, default=timezone.now)
    modificado_em = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        abstract = True


class FinanciamentoVeiculo(TimedModel):
    TIPOS_VEICULO = (
        ("carro", "Carro"),
        ("moto", "Moto"),
        ("utilitario", "Utilitário"),
        ("caminhao", "Caminhão"),
    )
    nome = models.CharField("Nome", max_length=300, null=True)
    cpf = models.CharField("CPF", max_length=100)
    email = models.EmailField("E-mail", default="")
    telefone = models.CharField("Telefone", max_length=100)

    tipo_veiculo = models.CharField(
        choices=TIPOS_VEICULO, max_length=100, default="carro"
    )
    valor_do_veiculo = models.CharField("Valor do Veículo", max_length=100)
    entrada = models.CharField("Valor de Entrada", max_length=100)
    ano = models.PositiveSmallIntegerField(default="")

    class Meta:
        verbose_name = "Financiamento de Veículo"
        verbose_name_plural = "Financiamentos de Veículos"

    def __str__(self):
        return f"Financiamento de Veículo: {self.cpf} - {self.valor_do_veiculo}"


class CartaoCredito(TimedModel):
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


class CapitalGiro(TimedModel):
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
