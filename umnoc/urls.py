"""
URLs for umnoc.
"""
from django.conf.urls import url
from .admin import umnoc_admin_site
from .api import api

urlpatterns = [
    # TODO: Fill in URL patterns and views here.
    # url(r'', TemplateView.as_view(template_name="umnoc/base.html")),

    url('^admin/', umnoc_admin_site.urls),
    url('^api/', api.urls)
]
