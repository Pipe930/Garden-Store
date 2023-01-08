from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['full_name'], body=data['message'], to=[data['email']])
        email.send()