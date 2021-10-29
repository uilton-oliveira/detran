# detran

Busca periodicamente por uma localidade ficar disponível para agendamento no detran.

Precisa obter o cookie primeiro simulando uma tentativa manual em https://www.detran.rj.gov.br/_monta_aplicacoes.asp?cod=15&tipo=agendamento_dic
Depois precisa configurar os secrets 'GMAIL_PASS' e 'COOKIE', que são necessários pra se logar no detran e também pra enviar o email avisando quando estiver disponível.

As demais propriedades (sender, dest, código da agência está hardcodeded no main.py)
O projeto é executado de hora em hora através de uma github action com uma cron definida.
