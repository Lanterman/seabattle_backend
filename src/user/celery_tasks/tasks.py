from django.core.mail import send_mail

from celery import shared_task

from config import settings


@shared_task
def send_account_activation(user_email: str, secret_key: str) -> None:
    link = f"http://127.0.0.1:8000/api/v1/auth/activate_account/{secret_key}/"
    html_message = f"""
        <p>
            You have been registered on our website.\n To activate your account, follow the link:\n
            <a href={link}>{link}</a>
        </p>
    """
    send_mail(
        subject=f'You have been registered on our website',
        message=html_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
        html_message=html_message,
    )