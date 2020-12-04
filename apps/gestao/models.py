
from django.db import models
# Create your models here.
from .constants import STATUS_CHOICES
from apps.users.models import Loja, User
from apps.porto.models import PropostaPorto
from apps.delta.helpers import currency_to_decimal

from .upload import UploadToPath


class Proposta(models.Model):
    aprovada_em = models.DateField(null=True)
    cliente = models.CharField(max_length=255)
    cpf_cnpj = models.CharField(max_length=255)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    telefone = models.CharField(max_length=255, blank=True)
    origem = models.CharField("Origem/Lead", max_length=255, blank=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, null=True, blank=True)


    valor_veiculo = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    valor_entrada = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    valor_financiado = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)

    veiculo = models.CharField(max_length=255, blank=True)
    parcelas = models.IntegerField(null=True, blank=True)
    valor_parcela = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    taxa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    n_contrato = models.CharField(max_length=255, blank=True)

    comissao = models.DecimalField(max_digits=3, decimal_places=1, default=6.0)
    comissao_operador = models.DecimalField(max_digits=3, decimal_places=2, default=2.0)

    valor_comissao = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    valor_comissao_operador = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    valor_comissao_liquido = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)


    arquivo_cnh = models.FileField("Arquivo da CNH", upload_to=UploadToPath("cnh"), null=True, blank=True)
    arquivo_nf = models.FileField("Dut ou NF", upload_to=UploadToPath("nf"),
                                   null=True, blank=True)
    arquivo_rg = models.FileField("Arquivo do RG", upload_to=UploadToPath("rg"), null=True, blank=True)
    arquivo_cpf = models.FileField("Arquivo do CPF", upload_to=UploadToPath("cpf"), null=True, blank=True)
    arquivo_endereco = models.FileField("Arquivo do Comprovante de Endereço", upload_to=UploadToPath("endereco"), null=True, blank=True)
    arquivo_renda = models.FileField("Arquivo do Comprovante de Renda", upload_to=UploadToPath("renda"), null=True, blank=True)
    arquivo_contrato_social = models.FileField("Arquivo do Contrato Social", upload_to=UploadToPath("contrato_social"), null=True, blank=True)




    criada_em = models.DateTimeField(auto_now_add=True)


    proposta_porto = models.OneToOneField(PropostaPorto, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.cpf_cnpj



    @classmethod
    def create_from_porto(cls, porto:PropostaPorto):
        self = cls()
        self.cliente = porto.nome
        self.cpf_cnpj = porto.cpf
        self.telefone = porto.celular if porto.celular else porto.telefone_fixo
        self.loja = ''
        self.valor_veiculo = currency_to_decimal(porto.valor_do_veiculo)
        self.valor_entrada = currency_to_decimal(porto.valor_de_entrada)
        self.valor_financiado = self.valor_veiculo - self.valor_entrada
        self.veiculo = porto.get_veiculo()
        self.parcelas = int(''.join([i for i in porto.prazo if i.isdigit()]))
        #self.valor_parcela = porto.nome
        #self.taxa = porto.nome
        #self.n_contrato = porto.nome
        #self.comissao = porto.nome
        #self.comissao_operador = porto.nome
        #self.valor_comissao = porto.nome

