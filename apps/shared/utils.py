import re
import threading

import phonenumbers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


def check_email(email):
    print(email)
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def check_username_email_or_phone(data):
    try:
        x = phonenumbers.parse(data)
        if phonenumbers.is_valid_number(x):
            return 'phone'
    except phonenumbers.NumberParseException:
        if re.fullmatch(regex, data):
            return 'email'
        else:
            return 'username'


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
            EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {'code': code}
    )
    Email.send_email(
        {
            'subject': "Ro'yxatdan o'tish",
            'to_email': email,
            'body': html_content,
            'content_type': "html",
        }
    )
