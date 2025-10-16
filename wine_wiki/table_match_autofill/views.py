from django.views import generic
from django.shortcuts import redirect
from . import forms
from django.urls import reverse_lazy
from . import models
from wine_wiki.models import WineListEdition, WineListDisplay
from .autofill import load_autofilleditions, load_autofillpending
from .models import AutoFillEditions, AutoFillPending
from django.http import HttpResponse


class StartAutoFillPickEditionView(generic.FormView):
    form_class = forms.StartFuzzyMatchListWikiForm
    template_name = "table_match_autofill/start_autofill.html"
    success_url = reverse_lazy("wine_wiki:autofill-show-editions")

    def form_valid(self, form):
        # TODO: add validation to ensure that the same edition cant be selected twice.

        if models.AutoFillRun.objects.all().count() > 0:
            models.AutoFillRun.objects.all().delete()

        wle_left = form.cleaned_data["left_edition"]
        wle_right = form.cleaned_data["right_edition"]

        load_autofilleditions(wle_left, wle_right)

        return super().form_valid(form)


class AutoFillShowPickedEditionsView(generic.ListView):
    model = AutoFillEditions
    context_object_name = "autofill_editions"
    template_name = "table_match_autofill/show_editions.html"

    def post(self, request):
        return redirect("wine_wiki:autofill-review")

    def get_context_data(self, **kwargs):
        """
        get some information about the left and right editions
        """
        context = super().get_context_data(**kwargs)
        obj_list = context["object_list"]
        afe = obj_list[0]

        edition_left = afe.edition_left
        edition_right = afe.edition_right
        right_edition_rows_with_wines = WineListDisplay.objects.filter(
            winelistraw__winelistedition=edition_right, wine__isnull=False
        ).count()
        left_edition_rows_with_wines = WineListDisplay.objects.filter(
            winelistraw__winelistedition=edition_left, wine__isnull=False
        ).count()

        context["edition_left"] = edition_left
        context["edition_right"] = edition_right
        context["right_edition_linked_row_count"] = right_edition_rows_with_wines
        context["left_edition_linked_row_count"] = left_edition_rows_with_wines

        return context


class AutoFillReview(generic.ListView):
    template_name = "table_match_autofill/autofill_review.html"
    model = AutoFillEditions
    # TODO: turn this into a form with match rejection.

    def get_context_data(self, **kwargs):
        """
        Main purpose is to run the auto join, update autofillpending and
        report the results.
        """
        # TODO: report results.
        #
        # what does that look like?
        # left input, right match, connected wine.

        context = super().get_context_data(**kwargs)

        # fetch the selected editions for matching
        wl_editions = context["object_list"][0]
        load_autofillpending(wl_editions=wl_editions)
        # get the loaded autofillpending rows into context.
        context["autofillpending"] = AutoFillPending.objects.all()

        return context
