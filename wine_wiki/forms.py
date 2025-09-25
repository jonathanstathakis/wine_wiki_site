from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FuzzyMatchListWiki, WineListUpload
from . import models
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


class StartFuzzyMatchListWikiForm(forms.Form):
    edition = forms.ModelChoiceField(queryset=models.WineListEdition.objects.all())


class FuzzyMatchListWikiResultsForm(forms.ModelForm):
    wine_list_query = forms.CharField(
        disabled=True,
        widget=forms.TextInput(attrs={"class": "results_form_field_readonly"}),
        required=False,
    )
    wiki_choice = forms.CharField(
        disabled=True,
        widget=forms.TextInput(attrs={"class": "results_form_field_readonly"}),
        required=False,
    )
    match_score = forms.CharField(
        disabled=True,
        widget=forms.TextInput(attrs={"class": "results_form_field_readonly"}),
        required=False,
    )

    wine_list = forms.ModelChoiceField(
        queryset=models.WineListDisplay.objects.all(), required=False
    )
    wiki = forms.ModelChoiceField(queryset=models.Wine.objects.all(), required=False)

    class Meta:
        model = models.FuzzyMatchListWiki
        fields = [
            "wine_list_query",
            "wiki_choice",
            "match_score",
            "review",
            "wine_list",
            "wiki",
        ]


FuzzyMatchListWikiResultsFormSet = forms.modelformset_factory(
    model=models.FuzzyMatchListWiki, form=FuzzyMatchListWikiResultsForm, extra=0
)
