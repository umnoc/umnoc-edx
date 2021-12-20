"""
Database models for umnoc.
"""
# from django.db import models
from .core.models import (Organization, OrganizationCourse, ProgramCourse, Direction, Project, TextBlock)
from .courses.models import (Course, Competence, Result, Author)
from .learners.models import (ProgramEnrollment)
from .profiles.models import (Profile, Reflection, Question, Answer)
