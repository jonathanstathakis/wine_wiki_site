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
    qs = FuzzyMatchListWiki.objects.all().order_by("-match_score")

    wle = qs[0].wine_list.winelistraw.winelistedition

    if request.method == "POST":
        formset = FuzzyMatchListWikiResultsFormSet(
            request.POST, request.FILES, queryset=qs
        )
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    review_val = form.cleaned_data["review"]
                    if review_val:
                        id = form.cleaned_data["id"].id

                        # update FuzzyMatchListWiki
                        match_result = FuzzyMatchListWiki.objects.get(id=id)
                        match_result.review = review_val
                        match_result.save()

                        # update winelistdisplay
                        wiki = match_result.wiki
                        list_wine = match_result.wine_list
                        list_wine.wine = wiki
                        list_wine.save()

            return HttpResponseRedirect("/fuzzy-match-list-wiki-summary/")
    else:
        formset = FuzzyMatchListWikiResultsFormSet(queryset=qs)

    return render(
        request=request,
        template_name="fuzzy_match/fuzzy_match_list_wiki_results.html",
        context={"formset": formset, "wle": wle},
    )


class FuzzyMatchlistWikiSummaryView(generic.ListView):
    """
    Provides a summary of results review - how many pairs were
    joined.
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
