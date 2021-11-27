"""
URLs for umnoc.
"""
from django.conf.urls import url

from .admin import umnoc_admin_site
from .api import api

urlpatterns = [
    url('^admin/', umnoc_admin_site.urls),
    url('^api/', api.urls),
]
