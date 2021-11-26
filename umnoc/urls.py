"""
URLs for umnoc.
"""
from .admin import umnoc_admin_site
from .api import api

urlpatterns = [
    # TODO: Fill in URL patterns and views here.
    # url(r'', TemplateView.as_view(template_name="umnoc/base.html")),

    path('umnoc_admin/', umnoc_admin_site.urls),
    path('api/', api.urls)
]
