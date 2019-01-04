from django.contrib.auth import forms as auth_forms
from django import forms
from . import models


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm):
        model = models.CustomUser
        fields = ('username','first_name' ,'last_name', 'email','ulica','kucni_broj','grad','drzava')
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserAuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )
        if not user.email_confirmed:
            raise forms.ValidationError(
                ("Sorry, you need to confirm your email."),
                code='emial_not_confirmed',
            )
    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
