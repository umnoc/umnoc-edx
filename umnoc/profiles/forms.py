from django.forms import ModelForm

from .models import Profile1


class ProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['SNILS'].error_messages = {
            "required": u"Введите СНИЛС",
            "invalid": u"Некорректно",
        }
        self.fields['specialty'].error_messages = {
            "required": u"Введите специальность (направление подготовки)",
            "invalid": u"Некорректно",
        }

    class Meta:
        model = Profile1
        fields = ['SNILS', 'specialty']
