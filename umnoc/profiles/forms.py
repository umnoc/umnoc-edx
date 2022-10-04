from django.forms import ModelForm

from .models import UrFUProfile


class UrFUProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UrFUProfileForm, self).__init__(*args, **kwargs)
        self.fields['SNILS'].error_messages = {
            "required": u"Введите СНИЛС",
            "invalid": u"Некорректно",
        }
        self.fields['specialty'].error_messages = {
            "required": u"Введите специальность (направление подготовки)",
            "invalid": u"Некорректно",
        }

    class Meta:
        model = UrFUProfile
        fields = ['SNILS', 'specialty', 'country', 'education_level', 'job', 'position', 'birth_date']
