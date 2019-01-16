from .models import Konferencija,User_Sekcija
from django.forms import ModelForm
from django import forms
from .models import CustomUser,Radovi
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
    description = forms.CharField(widget=forms.Textarea)
    summary = forms.CharField(widget=forms.Textarea)

    #sekcije = forms.MultipleChoiceField(choices=SAMPLE_CHOICES)
    class Meta:
        model = Konferencija
        fields = ['name','chairman','model_categories','image','description','summary']
    def __init__(self, *args, **kwargs):
        super(ConferenceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SekcijaForm(ModelForm):
    CHOICES = ((False, 'Normal User'),(True, 'Recenzent'),)
    recenzent = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = User_Sekcija
        fields = ['recenzent']
    def __init__(self, *args, **kwargs):
        super(SekcijaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UploadFileForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
    class Meta:
        model = Radovi
        fields = ['upload','title','authors']
