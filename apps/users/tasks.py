import logging
import os

from django import template

import requests
from celery import shared_task

logger = logging.getLogger(__name__)


mailgun_base_url = os.environ.get("MAILGUN_BASE_URL")
mailgun_api_key = os.environ.get("MAILGUN_API_KEY")
sender = os.environ.get("SENDER")


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_account_activation_email(
    self,
    email,
    otp,
    first_name,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    html_temp = template.loader.get_template("auth/account_activation.html")
    context = {"first_name": first_name, "otp": otp}
    html_content = html_temp.render(context)
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Activate your Fin-24 Account",
            "html": html_content,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.debug(response)
    except Exception as e:
        logger.error(e)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_new_otp_email(
    self,
    email,
    otp,
    first_name,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    html_temp = template.loader.get_template("auth/new_otp.html")
    context = {"first_name": first_name, "otp": otp}
    html_content = html_temp.render(context)
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Activate your Fin-24 Account",
            "html": html_content,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.debug(response)
    except Exception as e:
        logger.error(e)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_password_reset_otp_email(
    self,
    email,
    otp,
    first_name,
    mailgun_base_url=mailgun_base_url,
    mailgun_api_key=mailgun_api_key,
    sender=sender,
):
    html_temp = template.loader.get_template("auth/reset_password.html")
    context = {"first_name": first_name, "otp": otp}
    html_content = html_temp.render(context)
    try:
        mailing_data = {
            "from": sender,
            "to": email,
            "subject": "Reset your Fin-24 Account",
            "html": html_content,
        }
        response = requests.post(
            mailgun_base_url,
            auth=("api", mailgun_api_key),
            data=mailing_data,
        )
        logger.debug(response)
    except Exception as e:
        logger.error(e)
