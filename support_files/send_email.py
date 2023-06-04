import mimetypes
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders
from pathlib import Path
from datetime import datetime, date, time

from configurations import configuration_file as config
import os


def msg_attach(email_dict):
    email_msg = MIMEMultipart()
    email_msg["Subject"] = f"Message from user @{email_dict['user_username']}"

    for file in os.listdir(f"user_files/{str(email_dict['user_id'])}"):
        filename = os.path.basename(file)
        ftype, encoding = mimetypes.guess_type(file)
        file_type, subtype = ftype.split("/")

        if file_type == "text":
            with open(f"user_files/{str(email_dict['user_id']) + '/' + filename}") as file:
                file = MIMEText(file.read())
        elif file_type == "image":
            with open(f"user_files/{str(email_dict['user_id']) + '/' + filename}", "rb") as file:
                file = MIMEImage(file.read(), subtype)
        elif file_type == "application":
            with open(f"user_files/{str(email_dict['user_id']) + '/' + filename}", "rb") as file:
                file = MIMEApplication(file.read(), subtype)
        else:
            continue
        file.add_header('content-disposition', 'attachment', filename=f'{filename}')
        email_msg.attach(file)

    date_send = datetime.today().strftime("%d.%m.%Y %H:%M")
    email_msg.attach(MIMEText(f"Message sent: {str(date_send)}", "plain"))

    return email_msg.as_string()


def send_email(email_dict):
    EMAIL_INFO = [config.configuration_data["EMAIL_INFO"][0], config.configuration_data["EMAIL_INFO"][1]]

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    email_msg = msg_attach(email_dict)

    try:
        server.login(EMAIL_INFO[0], EMAIL_INFO[1])
        server.sendmail(EMAIL_INFO[0], email_dict["recipient"], email_msg)

    except Exception as _ex:
        return f"{_ex}\n Проверяй сука свои цифрые ебаные"


def main(sender_info_dict):
    send_email(sender_info_dict)

