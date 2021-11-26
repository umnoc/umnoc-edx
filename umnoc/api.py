from datetime import date
from uuid import uuid4

from ninja import NinjaAPI
from ninja import Schema

from .core.models import Program, Project

api = NinjaAPI()


class ProgramOut(Schema):
    uuid: uuid4
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
