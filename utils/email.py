import email
import smtplib, ssl
import email.message

import getpass
from decouple import config

email_address = config('EMAIL_USER')
password = config('EMAIL_PASSWORD')

def send_email(subject: str, message: str, to: str):
    context = ssl.create_default_context()
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.ehlo()
        server.login(email_address, password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string().encode())