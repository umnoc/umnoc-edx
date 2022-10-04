from django.forms import ModelForm
from .models import Profile1


class ProfileForm(ModelForm):
    class Meta:
        model = Profile1
        fields = ['SNILS', 'specialty']
