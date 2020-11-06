STAGE_1 = 1
STAGE_2 = 2
STAGE_3 = 3
STAGE_4 = 4
STAGE_5 = 5
STAGE_6 = 6
COMPLETE = 7

STAGE_ORDER = [STAGE_1, STAGE_2, STAGE_3, STAGE_4, STAGE_5, STAGE_6, COMPLETE]


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

COMBUSTIVEL = [("Gasolina/Alcool/Flex", "Gasolina/Alcool/Flex"), ("Diesel", "Diesel")]
CAMBIO = [("Manual", "Manual"), ("Automatico", "Automático")]


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
