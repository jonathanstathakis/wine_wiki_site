from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from wine_wiki.models import WineListDisplay

from .autofill import load_autofilleditions, load_autofillpending
from .forms import AutofillMatchResultsFormSet, AutoFillPickEditionsForm
from .models import AutoFillEditions, AutoFillPending, AutoFillRun


class StartAutoFillPickEditionView(generic.FormView):
    form_class = AutoFillPickEditionsForm
    template_name = "table_match_autofill/start_autofill.html"
    success_url = reverse_lazy("wine_wiki:autofill-show-editions")

    def form_valid(self, form):
        # TODO: add validation to ensure that the same edition cant be selected twice.

        if AutoFillRun.objects.all().count() > 0:
            AutoFillRun.objects.all().delete()

        wle_left = form.cleaned_data["left_edition"]
        wle_right = form.cleaned_data["right_edition"]

        load_autofilleditions(wle_left, wle_right)

        return super().form_valid(form)


class AutoFillShowPickedEditionsView(generic.ListView):
    model = AutoFillEditions
    context_object_name = "autofill_editions"
    template_name = "table_match_autofill/show_editions.html"

    def post(self, request):
        # assumes there is always only one row.
        wl_editions = self.get_queryset().values()[0]
        load_autofillpending(wl_editions=wl_editions)
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


def autofill_results_view(request):
    """
    written as function because class based form views don't appear to support
    formsets.

    TODO: documentation.
    """
    qs = AutoFillPending.objects.all()

    if request.method == "POST":
        formset = AutofillMatchResultsFormSet(request.POST, request.FILES, queryset=qs)
        if formset.is_valid():
            # for each row/form in the formset..
            for form in formset:
                # if the row's input is validated..
                if form.cleaned_data:
                    # get the value of review (whether the user accepts the result)
                    review_val = form.cleaned_data["review"]
                    # if user accepts..
                    if review_val:
                        # get the id of the row..
                        id = form.cleaned_data["id"].id

                        match_result = AutoFillPending.objects.get(id=id)
                        # set the review value to True
                        match_result.review = review_val
                        # save the result.
                        match_result.save()

                        # also update winelistdisplay to link it to the matched wiki entry.

            # redirect to the summary page.
            return redirect("wine_wiki:autofill-summary")
    # if a POST request is not made.. (don't know when this would happen)
    else:
        formset = AutofillMatchResultsFormSet(queryset=qs)

    # because forms work by first sending the render request then a second
    # request is made to do the POST action, the flow is inverted from expectations. Hence this return statement is the first thing that happens on page request.
    return render(
        request=request,
        template_name="table_match_autofill/autofill_review.html",
        context={"formset": formset},
    )


# TODO: define summary view, connect to process.
class AutofillSummaryView(generic.TemplateView):
    """
    Provides a summary of results review - how many pairs were
    joined.
    TODO: docs.
    wiki = match_result.wiki
    list_wine = match_result.wine_list_left
    list_wine.wine = wiki
    list_wine.save()
    """

    template_name = "table_match_autofill/autofill_summary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["autofill_pending_items"] = AutoFillPending.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        autofill_pending_items = AutoFillPending.objects.all()
        # TODO: complete post logic.
        for row in autofill_pending_items:
            wine_list_entry = row.wine_list_left
            wiki_entry = row.wiki
            wine_list_entry.wine_id = wiki_entry.id
            wine_list_entry.save()

        return redirect("wine_wiki:autofill-conclusion")


class AutofillConclusion(generic.TemplateView):
    template_name = "table_match_autofill/conclusion.html"
