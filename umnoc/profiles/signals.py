import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UrFUProfile

log = logging.getLogger(__name__)


@receiver(post_save, sender=UrFUProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # TODO: Send to Bitrix24 webhook
        try:
            webhook = f"https://{settings.BITRIX_URL}/rest/{settings.BITRIX_USER_ID}/{settings.BITRIX_WEBHOOK}/"
            b = Bitrix(webhook)
            method = 'crm.lead.add'
            params = {'fields': {'SNILS': instance.SNILS}}  # for sample
            b.call(method, params)
        except:
            log.warning(f"Cannot send request to Bitrix24: {instance.user}")
        log.warning(f"User profile created: {instance.user}")
