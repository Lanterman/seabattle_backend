from django.core.mail import send_mail
from smtplib import SMTPException

from celery import shared_task

from config import settings
from src.user import models


@shared_task
def send_account_activation(user_email: str, secret_key: str) -> None:
    html_message = f"""
        <p>
            You have been registered on our website.\n 
            To activate your account, enter the verification code on the site:\n
            <h3 >{secret_key}</h3>
        </p>
    """

    try:
        send_mail(
            subject=f'You have been registered on our website',
            message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
            html_message=html_message,
        )
    except SMTPException:
        models.User.objects.filter(email=user_email).delete()
