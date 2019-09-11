from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Recruiter
from django.forms import ModelForm

class SignUpForm(ModelForm):
    class Meta:
        model = Recruiter
        fields = ('organization', 'first_name', 'last_name', 'email' )