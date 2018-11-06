from .models import conference
from django.forms import ModelForm
from django import forms
from .models import CustomUser
class ConferenceForm(ModelForm):
    chairman = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    class Meta:
        model = conference
        fields = ['name','chairman']
