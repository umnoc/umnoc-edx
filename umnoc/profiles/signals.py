import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UrFUProfile

log = logging.getLogger(__name__)


@receiver(post_save, sender=UrFUProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # TODO: Send to Bitrix24 webhook
        log.warning(f"User Profile Created: {instance.SNILS}")
