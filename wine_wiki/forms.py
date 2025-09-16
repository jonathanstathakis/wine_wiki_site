from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WineListUpload


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]


class WineListUploadForm(forms.ModelForm):
    class Meta:
        model = WineListUpload
        fields = ["file", "name"]
