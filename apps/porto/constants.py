from collections import namedtuple
from enum import Enum


STAGE_1_PF = '1_pf'
STAGE_1_PJ = '1_pj'
STAGE_2 = '2'
STAGE_3 = '3'
STAGE_4 = '4'
STAGE_5_PF = '5_pf'
STAGE_5_PJ = '5_pj'

STAGE_6 = '6'
COMPLETE = '7'

STAGE_ORDER_PF = [STAGE_1_PF, STAGE_2, STAGE_3, STAGE_4, STAGE_5_PF, STAGE_6, COMPLETE]
STAGE_ORDER_PJ = [STAGE_1_PJ, STAGE_2, STAGE_3, STAGE_4, STAGE_5_PJ, STAGE_6, COMPLETE]



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



RENDA_ASSALARIADO = "assalariado"
RENDA_AUTONOMO = "autonomo"
RENDA_EMPRESARIO = "empresario"
RENDA_APOSENTADO = "aposentado"

TIPO_RENDA = [
    (RENDA_ASSALARIADO, "assalariado"),
    (RENDA_AUTONOMO, "autônomo"),
    (RENDA_EMPRESARIO, "empresário"),
    (RENDA_APOSENTADO, "aposentado"),
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

COMBUSTIVEL = [
    ("Gasolina/Alcool/Flex", "Gasolina/Alcool/Flex"),
    ("Hibrido", "Hibrido"),
    ("Eletrico", "Elétrico"),
]

CAMBIO = [("Manual", "Manual"), ("Automatico", "Automático")]
ANOS = 20

VALIDATE_PLACA_MIN = VALIDATE_PLACA_MAX = 7
VALIDATE_RENAVAM_MIN = 9
VALIDATE_RENAVAM_MAX = 11
VALIDATE_CHASSI_MIN = 17
VALIDATE_CHASSI_MAX = 17

State = Enum("State", "INICIAL ERRO RECUSADO APROVADO PRE_APROVADO")

SIMULACAO_INICIAL = 1
SIMULACAO_ERRO = 2
SIMULACAO_RECUSADO = 3
SIMULACAO_APROVADO = 4
SIMULACAO_PRE_APROVADO = 5

STATUS_SIMULACAO = [
    (SIMULACAO_INICIAL, "Inicial"),
    (SIMULACAO_ERRO, "Erro"),
    (SIMULACAO_RECUSADO, "Recusado"),
    (SIMULACAO_APROVADO, "Aprovado"),
    (SIMULACAO_PRE_APROVADO, "Credito Pre Aprovado"),
]


STATUS_NAO_SIMULADO = 1
STATUS_ERRO = 2
STATUS_PRE_RECUSADO = 3
STATUS_EM_DIGITACAO = 4

STATUS = [
    (STATUS_NAO_SIMULADO, "Não simulado"),
    (STATUS_ERRO, "Erro"),
    (STATUS_PRE_RECUSADO, "Pre Recusado"),
    (STATUS_EM_DIGITACAO, "Em Digitação"),
]


Valores = namedtuple("Valores", ["valor", "entrada", "cpf"])
ResultadoSimulacao = namedtuple(
    "ResultadoSimulacao", ["estado", "parcelas", "mensagem"]
)
