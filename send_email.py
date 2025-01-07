from email.header import Header
from email.mime.text import MIMEText
import smtplib


def send_email(to, subject, body, user_state_update):
    msg = MIMEText(body.encode('utf-8'), _charset='UTF-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = user_state_update['email']
    msg['To'] = to

    mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
    mailserver.ehlo()
    mailserver.starttls()  # Включаем защищенное соединение TLS
    mailserver.login(user_state_update['email'], user_state_update['password'])
    mailserver.sendmail(user_state_update['email'], [to], msg.as_string())
    mailserver.quit()

    return True
