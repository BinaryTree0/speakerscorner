from .models import conference
from django.forms import ModelForm
from django import forms
from .models import CustomUser
class ConferenceForm(ModelForm):
    MODEL_CATEGORIES = (
        ('maths', 'maths'),
        ('history', 'history'),
        ('science', 'science'),
    )
    model_categories = forms.MultipleChoiceField(
            widget = forms.CheckboxSelectMultiple,
            choices = MODEL_CATEGORIES
    )
    chairman = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    #sekcije = forms.MultipleChoiceField(choices=SAMPLE_CHOICES)
    class Meta:
        model = conference
        fields = ['name','chairman','model_categories']
