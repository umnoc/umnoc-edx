from datetime import date
from typing import List

from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema

from .core.models import Program, Project, Organization

api = NinjaAPI()


class OrganizationSchema(ModelSchema):
    class Config:
        model = Organization
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'logo', 'image_background', 'status']


class ProgramSchema(ModelSchema):
    owner: OrganizationSchema

    class Config:
        model = Program
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'number_of_hours', 'logo',
                        'image_background',
                        'edu_start_date', 'edu_end_date', 'issued_document_name', 'enrollment_allowed', 'owner']


@api.get("/programs", response=List[ProgramSchema])
def programs(request):
    qs = Program.objects.filter(active=True, status='published')
    return qs
