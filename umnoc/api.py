from datetime import date
from typing import List

from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema

from .core.models import Program, Project

api = NinjaAPI()


class ProgramSchema(ModelSchema):
    class Config:
        model = Program
        model_fields = ['uuid', 'title', 'short_name', 'slug', 'description', 'number_of_hours', 'logo',
                        'edu_start_date', 'edu_end_date']


@api.get("/programs")
def programs(request, response=List[ProgramSchema]):
    qs = Program.objects.filter(active=True, status='published')
    return qs
