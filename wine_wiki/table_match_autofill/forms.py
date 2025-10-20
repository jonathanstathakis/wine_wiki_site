from django import forms
from .models import AutoFillPending
from wine_wiki.models import WineListDisplay, WineListEdition, Wine


class AutoFillPickEditionsForm(forms.Form):
    left_edition = forms.ModelChoiceField(queryset=WineListEdition.objects.all())

    right_edition = forms.ModelChoiceField(queryset=WineListEdition.objects.all())


class AutofillMatchResultsForm(forms.ModelForm):
    wine_list_left = forms.ModelChoiceField(
        queryset=WineListDisplay.objects.all(),
        required=False,
    )
    wine_list_right = forms.ModelChoiceField(
        queryset=WineListDisplay.objects.all(),
        required=False,
    )
    wiki = forms.ModelChoiceField(queryset=Wine.objects.all(), required=False)

    class Meta:
        model = AutoFillPending
        fields = [
            "wine_list_left",
            "wine_list_right",
            "wiki",
            "review",
        ]


# TODO: continue trying to fix this form. DOnt really undesrstand how modelchoicefield works but we'er currently getting not unique errors.. autofill is matching duplicates?
AutofillMatchResultsFormSet = forms.modelformset_factory(
    model=AutoFillPending, form=AutofillMatchResultsForm, extra=0
)
