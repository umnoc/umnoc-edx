from django.shortcuts import render
from django.views.generic import View

from .models import ExternalPlatform


class GetExternalCourses(View):
    """
    Редиректит на поддомен edu
    """

    def get(self, request, *args, **kwargs):
        context = {}
        sources = ExternalPlatform.objects.all()
        context['sources'] = sources
        return render(request, 'umnoc_edx/staff/external_courses.html', context=context)
