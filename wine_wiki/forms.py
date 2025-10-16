from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WineListUpload
from django.core.exceptions import ValidationError
from pathlib import Path


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name"]


def validate_file(in_memory_file):
    """
    validate that the file path suffix is '.csv'
    """

    if not Path(in_memory_file.name).suffix == ".csv":
        raise ValidationError("file not a csv file.")


class WineListUploadForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file])

    class Meta:
        model = WineListUpload
        fields = ["name", "file"]


class WineListRawIngestionForm(forms.Form):
    winelistupload = forms.ModelChoiceField(queryset=WineListUpload.objects.all())
