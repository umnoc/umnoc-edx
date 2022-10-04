"""
umnoc Django application initialization.
"""

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class UmnocEdxConfig(AppConfig):
    """
    Configuration for the umnoc Django application.
    """

    name = 'umnoc'

    def ready(self):
        import umnoc.profile.signals


class UMNOCAdminConfig(AdminConfig):
    # default_site = 'umnoc.admin.UMNOCAdminSite'
    name = 'umnoc.admin.UMNOCAdminSite'
    label = 'umnoc_admin'
