import os
import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup


class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = os.getenv('GMAIL_USER')
        self.password = os.getenv('GMAIL_PASS')

    def send(self, email, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        msg = MIMEMultipart('alternative')
        msg.set_charset('utf8')

        msg['FROM'] = self.sender_mail
        msg['To'] = email
        msg['Subject'] = Header(
            subject.encode('utf-8'),
            'UTF-8'
        ).encode()
        msg.attach(MIMEText(content.encode('utf-8'), 'plain', 'UTF-8'))

        service.sendmail(self.sender_mail, email, msg.as_string())
        service.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r = requests.post(
        'https://www2.detran.rj.gov.br/portal/identificacao_civil/agendamentoListaPostos',
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "X-Requested-With": "XMLHttpRequest",
            "X-Prototype-Version": "1.7",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Update": "divPostos",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "referrer": "https://www2.detran.rj.gov.br/portal/IdentificacaoCivil/agendamentoMunicipio",
        },
        data='data%5BidentificacaoCivil%5D%5BcoMunicipio%5D=3280',
        cookies={
            'CAKEPHP': os.getenv('COOKIE'),
            'PHPSESSID': os.getenv('COOKIE')
        },
        verify=False
    )
    soup = BeautifulSoup(r.text, features="html.parser")
    input_meier = soup.find("input", {"id": "posto303"})
    if input_meier is not None:
        # https://www.detran.rj.gov.br/_monta_aplicacoes.asp // lista de postos
        # https://www.detran.rj.gov.br/_monta_aplicacoes.asp?cod=15&tipo=lista_posto_ic&codigo=303&municipio=3280&bairro=M%C3%A9ier
        # 303 = Meier
        print("Found!")
        name = input_meier.next.strip()
        date = input_meier.parent.find("span", {"class": "spanLabel"}).text.split()[0]
        print(f'- {name} / {date}')

        mail = Mail()
        mail.send(
            'uilton.dev@gmail.com',
            'Detran Meier disponivel!',
            f"""
            Detran {name} disponível na data {date}, correee!!
            """)
    else:
        print("Not found, listing all available options:")
        inputs = soup.find_all("input", {"type": "radio"})
        for input in inputs:
            name = input.next.strip()
            date = input.parent.find("span", {"class": "spanLabel"}).text.split()[0]
            print(f'- {name} / {date}')
