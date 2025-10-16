from . import fuzzy_match_list_wiki
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from wine_wiki.models import WineListEdition, WineListDisplay

from .forms import StartFuzzyMatchListWikiForm, FuzzyMatchListWikiResultsFormSet
from .models import FuzzyMatchListWiki

logger = logging.getLogger(__name__)


class StartFuzzyMatchListWikiView(generic.FormView):
    """
    first view of the fuzzy match process. Simply requests the user to select a wine list edition. On successful submission runs the fuzzy match for that edition, storing the results in FuzzyMatchListWiki.
    """

    form_class = StartFuzzyMatchListWikiForm
    template_name = "fuzzy_match/start_fuzzy_match_wine_list_wine_wiki.html"
    success_url = reverse_lazy("wine_wiki:fuzzy-match-list-wiki-results")

    def form_valid(self, form):
        if FuzzyMatchListWiki.objects.all().count() > 0:
            FuzzyMatchListWiki.objects.all().delete()

        wle = form.cleaned_data["edition"]

        fuzzy_match_list_wiki.fuzzy_match_list_wiki(wle=wle)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        need to define the queryset.
        """
        latest_pub_date = WineListEdition.objects.order_by("-pub_date").values()[0][
            "pub_date"
        ]
        context = super().get_context_data(**kwargs)
        context["pub_date"] = latest_pub_date.strftime("%Y-%m-%d")

        wine_list_not_linked = WineListDisplay.objects.filter(
            winelistraw__winelistedition__pub_date=latest_pub_date, wine_id=None
        )
        context["num_wines_not_linked"] = len(wine_list_not_linked)
        return context


def fuzzymatchlistwiki_review_view(request):
    """
    written as function because class based form views don't appear to support
    formsets.

    Displays the results of the preceeding fuzzy match computation through a
    table rendered formset where each row is a row of the selected wine list
    edition, its corresponding match, and a checkbox column titled 'review'
    that the user can use to accept the result. On clicking submit the data
    entered into the formset, in this case whether the box is checked or not,
    is used to decide whether to update winelistdisplay to link it to the
    matched wine. The results are also stored in the fuzzymatchresults table.
    On completion of the POST request the user is redirected to a summary page.
    """
    # get all fuzzymatch results ordered by match score descending
    qs = FuzzyMatchListWiki.objects.all().order_by("-match_score")

    # get the current wine list edition from the first row of the qs
    # this is used to display the edition publication date at the top
    # of the page.
    wle = qs[0].wine_list.winelistraw.winelistedition

    if request.method == "POST":
        # generate a formset from the fuzzy match results
        formset = FuzzyMatchListWikiResultsFormSet(
            request.POST, request.FILES, queryset=qs
        )
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

                        ## update FuzzyMatchListWiki
                        # get the match result row corresponding to the accepted result in the formset..
                        match_result = FuzzyMatchListWiki.objects.get(id=id)
                        # set the review value to True
                        match_result.review = review_val
                        # save the result.
                        match_result.save()

                        # also update winelistdisplay to link it to the matched wiki entry.
                        wiki = match_result.wiki
                        list_wine = match_result.wine_list
                        list_wine.wine = wiki
                        list_wine.save()

            # redirect to the summary page.
            return HttpResponseRedirect("/fuzzy-match-list-wiki-summary/")
    # if a POST request is not made.. (don't know when this would happen)
    else:
        formset = FuzzyMatchListWikiResultsFormSet(queryset=qs)

    # because forms work by first sending the render request then a second
    # request is made to do the POST action, the flow is inverted from expectations. Hence this return statement is the first thing that happens on page request.
    return render(
        request=request,
        template_name="fuzzy_match/fuzzy_match_list_wiki_results.html",
        context={"formset": formset, "wle": wle},
    )


class FuzzyMatchlistWikiSummaryView(generic.ListView):
    """
    Provides a summary of results review - how many pairs were
    joined.
    Simply displays the results stored in FuzzyMatchListWiki.
    """

    model = FuzzyMatchListWiki
    fields = "__all__"
    template_name = "fuzzy_match/fuzzy_match_list_wiki_summary.html"
    context_object_name = "match_results"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        object_list = context["match_results"]

        wle = object_list[0].wine_list.winelistraw.winelistedition
        context["wle"] = wle

        matched_pairs = []
        unmmatched_pairs = []

        for obj in object_list:
            if obj.review:
                matched_pairs.append(obj)
            else:
                unmmatched_pairs.append(obj)

        context["matched_pairs"] = matched_pairs
        context["unmatched_pairs"] = unmmatched_pairs

        return context
