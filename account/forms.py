from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] == cd['password2']:
            return cd['password2']
        else:
            raise ValidationError('Passwords doesn\'t match')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            if User.objects.filter(email = email).exists():
                return None
            return email
            
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

        

class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'name',
        ]