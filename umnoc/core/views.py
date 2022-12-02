from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import ExternalPlatform


class GetExternalCourses(View):
    """
    Редиректит на поддомен edu
    """

    def get(self, request, *args, **kwargs):
        context = {}
        sources = ExternalPlatform.objects.all()
        context['sources'] = sources
        return render(request, template_name='umnoc_edx/staff/external_courses.html', context=context)

    def post(self, request, *args, **kwargs):
        external_course_id = request.POST("external_course_id")
        return HttpResponse(external_course_id)

