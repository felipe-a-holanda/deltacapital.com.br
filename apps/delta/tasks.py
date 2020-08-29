from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from config import celery_app


logger = get_task_logger(__name__)



@celery_app.task
def send_default_email(object, subject="", to_email=None):

    msg_plain = render_to_string("delta/emails/email.txt", {"object": object})
    msg_html = render_to_string("delta/emails/email.html", {"object": object})

    from_email = settings.DEFAULT_FROM_EMAIL
    if not to_email:
        to_email = settings.DEFAULT_TO_EMAIL
    prefix = settings.EMAIL_SUBJECT_PREFIX

    nome = object.get("Nome", "")

    subject_email = f"{prefix} {subject} {nome}"

    send_mail(subject_email, msg_plain, from_email, [to_email], html_message=msg_html)

    logger.info(f"Email sent [{subject}]")
    logger.info(f"{msg_plain}")
    logger.info(f"{msg_html}")

