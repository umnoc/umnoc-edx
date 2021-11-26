from datetime import date
from typing import List

from ninja import NinjaAPI
from ninja import Schema

from .core.models import Program, Project

api = NinjaAPI()


class ProgramOut(Schema):
    uuid: str
    title: str
    short_name: str
    slug: str
    description: str
    logo: str
    number_of_hours: int
    edu_start_date: date = None
    edu_end_date: date = None


@api.get("/programs")
def programs(request, response=List[ProgramOut]):
    qs = Program.objects.filter(active=True, status='published')
    return qs
