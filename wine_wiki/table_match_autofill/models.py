# TODO: define autofill model
# TODO: define autofill view
# TODO: define autofill review view
from wine_wiki.models import Wine, WineListDisplay, WineListEdition
from django.db import models


class AutoFillRun(models.Model):
    """
    represents a run instance of the autofill process. Only expect 1
    row at a time, cleared on beginning of a new run.
    """

    pass


class AutoFillEditions(models.Model):
    """
    the editions of the autofill run, left edition is updated from
    right edition. Expectation is that left is newer than right.
    """

    autofillrun = models.ForeignKey(to=AutoFillRun, on_delete=models.CASCADE)
    edition_left = models.ForeignKey(
        to=WineListEdition, on_delete=models.CASCADE, related_name="edition_left"
    )
    edition_right = models.ForeignKey(
        to=WineListEdition, on_delete=models.CASCADE, related_name="edition_right"
    )


class AutoFillPending(models.Model):
    """
    A staging table containing the results of the self join linkin the left edition
    wine list rows to the right editions already joined wines.
    """

    autofilledition = models.ForeignKey(to=AutoFillEditions, on_delete=models.CASCADE)
    wine_list_left = models.OneToOneField(
        to=WineListDisplay,
        on_delete=models.CASCADE,
        related_name="wld_left",
    )
    wine_list_right = models.ForeignKey(
        to=WineListDisplay,
        on_delete=models.CASCADE,
        related_name="wld_right",
    )
    wiki = models.OneToOneField(to=Wine, on_delete=models.CASCADE, null=True)
    review = models.BooleanField(default=True)
