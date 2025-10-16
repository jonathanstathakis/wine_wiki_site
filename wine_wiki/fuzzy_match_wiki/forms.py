from django import forms
from .models import FuzzyMatchListWiki
from wine_wiki.models import Wine, WineListEdition, WineListDisplay


class StartFuzzyMatchListWikiForm(forms.Form):
    edition = forms.ModelChoiceField(queryset=WineListEdition.objects.all())


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
        queryset=WineListDisplay.objects.all(), required=False
    )
    wiki = forms.ModelChoiceField(queryset=Wine.objects.all(), required=False)

    class Meta:
        model = FuzzyMatchListWiki
        fields = [
            "wine_list_query",
            "wiki_choice",
            "match_score",
            "review",
            "wine_list",
            "wiki",
        ]


FuzzyMatchListWikiResultsFormSet = forms.modelformset_factory(
    model=FuzzyMatchListWiki, form=FuzzyMatchListWikiResultsForm, extra=0
)
