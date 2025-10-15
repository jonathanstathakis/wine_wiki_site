from django import forms
from wine_wiki import models


class StartFuzzyMatchListWikiForm(forms.Form):
    left_edition = forms.ModelChoiceField(queryset=models.WineListEdition.objects.all())

    right_edition = forms.ModelChoiceField(
        queryset=models.WineListEdition.objects.all()
    )
