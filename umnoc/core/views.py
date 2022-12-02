from django.shortcuts import render
from django.views.generic import View

from .models import ExternalPlatform
from django.contrib.admin.views.decorators import staff_member_required

class GetExternalCourses(View):
    """
    Редиректит на поддомен edu
    """

    def get(self, request, *args, **kwargs):
        context = {}
        sources = ExternalPlatform.objects.all()
        context['sources'] = sources
        return render(request, template_name='umnoc_edx/staff/external_courses.html', context=context)

@staff_member_required
def assimilate(request):
    if request.method.upper() == "POST":

