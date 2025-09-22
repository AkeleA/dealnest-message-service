import logging
from . import config

settings = config.settings
log = logging.getLogger("emailer")

def send_email(to_email: str, subject: str, body: str):
    log.info("MOCK EMAIL -> to=%s subject=%r body=%r sender=%s",
             to_email, subject, body, settings.EMAIL_SENDER)
