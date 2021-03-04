STATUS = (
    ("aguardando", "Aguardando Análise", "yellow"),
    ("analista", "Com Analista", "orange"),
    ("recusado", "Recusado", "red"),
    ("reanalise", "Em Reanálise", "purple"),
    ("aprovado", "Aprovado", "green"),
    ("efetivada", "Proposta Efetivada", "blue"),
)

RETORNOS = ["0.0", "0.6", "1.2", "1.8", "2.4", "3.0", "3.6", "4.2", "4.8", "5.4", "6.0"]

STATUS_CHOICES = [i[:2] for i in STATUS]
STATUS_COLORS = {i[0]: i[2] for i in STATUS}
