import asyncio
import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from fast_bitrix24 import Bitrix

from .models import UrFUProfile

log = logging.getLogger(__name__)


@receiver(post_save, sender=UrFUProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # TODO: Send to Bitrix24 webhook
        # try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        webhook = f"{settings.BITRIX_URL}rest/{settings.BITRIX_USER_ID}/{settings.BITRIX_WEBHOOK}/"
        log.warning(f'BITRIX24 !!!!!!!!!!!!!!!! {webhook}')
        b = Bitrix(webhook)
        method = 'crm.lead.add'
        params = {'fields': {
            'TITLE': 'УМНОЦ лид',
            'NAME': instance.first_name,
            'SECOND_NAME': instance.second_name,
            'LAST_NAME': instance.last_name,
            'STATUS_ID': 'NEW',
            'EMAIL': [{'ID': instance.user.id, 'VALUE': instance.user.email, 'VALUE_TYPE': 'WORK'}],
            'PHONE': [{'ID': instance.user.id, 'VALUE': instance.phone, 'VALUE_TYPE': 'MOBILE'}]
        }}
        b.call(method, params)
        # except:
        #     log.warning(f"Cannot send request to Bitrix24: {instance.user}")
        log.warning(f"User profile created: {instance.user}")
