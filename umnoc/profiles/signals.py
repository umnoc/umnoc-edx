import asyncio
import logging

from django.conf import settings
from django.db.models.signals import post_save
from fast_bitrix24 import Bitrix
from django.contrib.auth.models import User
from .models import UrFUProfile, LeadRequest
from django.dispatch import receiver

log = logging.getLogger(__name__)


@receiver(post_save, sender=UrFUProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        webhook = f'{settings.BITRIX_URL}rest/{settings.BITRIX_USER_ID}/{settings.BITRIX_WEBHOOK}/'
        b = Bitrix(webhook)
        method = 'crm.lead.add'
        status_id = 'NEW',
        params = {'fields': {
            'TITLE': settings.BITRIX_LEAD_TITLE_DEFAULT,
            'NAME': instance.first_name,
            'SECOND_NAME': instance.second_name,
            'LAST_NAME': instance.last_name,
            'STATUS_ID': status_id,
            'EMAIL': [{'ID': instance.user.id, 'VALUE': instance.user.email, 'VALUE_TYPE': 'WORK'}],
            'PHONE': [{'ID': instance.user.id, 'VALUE': instance.phone, 'VALUE_TYPE': 'MOBILE'}]
        }}
        request = LeadRequest.objects.create(
            method=method,
            title=settings.BITRIX_LEAD_TITLE_DEFAULT,
            name=instance.first_name,
            second_name=instance.second_name,
            last_name=instance.last_name,
            status_id=status_id,
            email=instance.user.email,
            phone=instance.phone
        )
        try:
            b.call(method, params)
            request.set_status('sent')
        except:
            log.error(f'Cannot send request to Bitrix24: {instance.user}')
            request.set_status("error")

        log.warning(f'User profile created: {instance.user}')


# @receiver(post_save, sender=User)
# def create_profile(*args, **kwargs):
#     UrFUProfile.objects.create(user=kwargs['instance'])
#

@receiver(post_save, sender=User)
def save_profile(*args, **kwargs):
    user = kwargs['instance']
    try:
        verified_profile = user.verified_profile
    except User._meta.model.related_field.RelatedObjectDoesNotExist as e:
        verified_profile = UrFUProfile.objects.create(user=kwargs['instance'])
        verified_profile.save()
