from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    #email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model=User
        fields=('username','email','password1','password2')
