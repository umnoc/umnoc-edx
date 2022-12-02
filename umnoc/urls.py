"""
URLs for umnoc.
"""
from django.conf.urls import url, include

from .admin import umnoc_admin_site
from .api import api
from .core.views import GetExternalCourses

urlpatterns = [
    url('^admin/', umnoc_admin_site.urls),
    url('^api/', api.urls),
    url('^summernote/', include('django_summernote.urls')),
    url('^ext/', GetExternalCourses.as_view())
]
