from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import (
    WineListDisplay,
    Producer,
    Wine,
    Variety,
    WineListEdition,
    WineListRaw,
)
from django.urls import reverse, reverse_lazy
from .forms import WineListRawIngestionForm, WineListUploadForm
from django.contrib import messages
from django.db.models import Q
import csv
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


class WineView(generic.DetailView):
    model = Wine
    template_name = "wine_wiki/wine.html"
    context_object_name = "wine"


class WineListView(generic.ListView):
    model = Wine
    template_name = "wine_wiki/wine-list.html"

    def get_queryset(self):
        """
        use the search form in wine_list.html to filter
        the wines present in db.
        """

        query = self.request.GET.get("q")
        if query:
            object_list = Wine.objects.filter(
                Q(base_year__icontains=query)
                | Q(classification__icontains=query)
                | Q(commune__icontains=query)
                | Q(disgorg_year__icontains=query)
                | Q(producer__name__icontains=query)
                | Q(region__icontains=query)
                | Q(variety__name__icontains=query)
                | Q(series__icontains=query)
                | Q(state__icontains=query)
                # TODO: figure out how to search tags
                | Q(tags__name__icontains=query)
                | Q(vineyard__icontains=query)
                | Q(vintage__icontains=query)
                | Q(volume__icontains=query)
                | Q(wine_name__icontains=query)
            )
        else:
            object_list = Wine.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q")

        object_list = context["object_list"]

        context["object_list"] = object_list.select_related(
            "producer",
            "variety",
        ).prefetch_related("tags")  # if you want tags

        context["query"] = query
        return context


class WineListDisplayDetailView(generic.DetailView):
    template_name = "wine_wiki/bennelong_wine_list_detail.html"
    context_object_name = "wine"

    # def get_queryset(self):
    #     latest_pub_date = WineListEdition.objects.order_by("-pub_date").values()[0][
    #         "pub_date"
    #     ]
    #     qs = WineListDisplay.objects.filter(
    #         winelistraw__winelistedition__pub_date=latest_pub_date
    #     )
    #     return qs


class WineListDisplayView(generic.ListView):
    """
    The display for the Bennelong wine list.
    """

    # TODO: add edition selector. Default to latest edition
    # but provide option as a drop down at the top to select
    # prior editions.
    # TODO: add url link to linked wine.
    # TODO: provide summary stats at top of page.
    # TODO: search bar
    # TODO: table of contents.

    model = WineListDisplay
    template_name = "wine_wiki/bennelong_wine_list.html"
    context_object_name = "wine_list"

    def get_queryset(self):
        """
        use the search form in wine_list.html to filter the wines present
        in db.
        """

        # default is to work with the latest published edition.
        # TODO: add ability to select editions.

        latest_pub_date = WineListEdition.objects.order_by("-pub_date").values()[0][
            "pub_date"
        ]
        qs = WineListDisplay.objects.filter(
            winelistraw__winelistedition__pub_date=latest_pub_date
        )

        query = self.request.GET.get("q")

        if query:
            object_list = qs.filter(
                Q(wine__base_year__icontains=query)
                | Q(wine__classification__icontains=query)
                | Q(wine__commune__icontains=query)
                | Q(wine__disgorg_year__icontains=query)
                | Q(wine__producer__name__icontains=query)
                | Q(wine__region__icontains=query)
                | Q(wine__variety__name__icontains=query)
                | Q(wine__series__icontains=query)
                | Q(wine__state__icontains=query)
                | Q(wine__tags__name__icontains=query)
                | Q(wine__vineyard__icontains=query)
                | Q(wine__vintage__icontains=query)
                | Q(wine__volume__icontains=query)
                | Q(wine__wine_name__icontains=query)
            )
        else:
            object_list = qs

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # object_list = context["object_list"]

        # wine_list = (
        #     object_list.select_related(
        #         "wine",
        #         "wine__producer",
        #         "wine__variety",
        #     ).prefetch_related("wine__tags")  # if you want tags
        # )

        # grouped = defaultdict(lambda: defaultdict(list))
        #
        # for row in wine_list:
        #     grouped[row.section][row.subsection].append(row.wine)
        #
        # # have to pass a dict to context rather than defaultdict
        # context["grouped_wines"] = {
        #     str(k): {str(u): w for u, w in v.items()} for k, v in grouped.items()
        # }
        #
        # context["grouped_wines"] = object_list

        # to display search term to user after searching.

        query = self.request.GET.get("q")
        context["query"] = query

        return context


class WineUpdateView(generic.UpdateView):
    model = Wine
    fields = "__all__"
    template_name = "wine_wiki/wine_update.html"

    def get_success_url(self):
        return reverse("wine_wiki:wine", kwargs={"pk": self.object.pk})


class WineCreateView(generic.CreateView):
    model = Wine
    fields = "__all__"
    template_name = "wine_wiki/wine_create.html"

    def get_success_url(self):
        return reverse("wine_wiki:wine", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The wine was created successfully.")
        return super(WineCreateView, self).form_valid(form)


class ProducerCreateView(generic.CreateView):
    model = Producer
    fields = "__all__"
    template_name = "wine_wiki/prod_create.html"

    def get_success_url(self):
        return reverse("wine_wiki:producer", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The producer was created successfully.")
        return super(ProducerCreateView, self).form_valid(form)


class ProducerUpdateView(generic.UpdateView):
    model = Producer
    fields = "__all__"
    template_name = "wine_wiki/prod_update.html"

    def get_success_url(self):
        return reverse("wine_wiki:producer", kwargs={"pk": self.object.pk})


class WineDeleteView(generic.DeleteView):
    model = Wine
    success_url = reverse_lazy("wine-wiki:wine-list")
    template_name = "wine_wiki/wine-delete.html"


class ProducerDeleteView(generic.DeleteView):
    model = Producer
    success_url = reverse_lazy("wine-wiki:producer-list")
    template_name = "wine_wiki/prod_delete.html"


# class SignUpView(SuccessMessageMixin, CreateView):
#     """
#     See <https://stackoverflow.com/questions/62935406/how-to-make-a-signup-view-using-class-based-views-in-django>.
#     """
#
#     template_name = "wine_wiki/registration/login.html"
#     success_url = reverse_lazy("login")
#     form_class = UserRegisterForm
#     success_message = "Your profile was created successfully"j
# views.py


class ProducerView(generic.DetailView):
    model = Producer
    template_name = "wine_wiki/producer.html"
    context_object_name = "producer"


class ProducerListView(generic.ListView):
    model = Producer
    template_name = "wine_wiki/producer_list.html"


class VarietyView(generic.DetailView):
    model = Variety
    template_name = "wine_wiki/variety.html"
    context_object_name = "variety"


class VarietyListView(generic.ListView):
    """
    TODO: turn "" variety into clickable hyperlink - *unassigned*
    or similar.
    """

    model = Variety
    template_name = "wine_wiki/variety_list.html"


from .models import WineListUpload


class WineListUploadListView(generic.ListView):
    model = WineListUpload
    template_name = "wine_wiki/winelistupload_list.html"


class WineListUploadView(generic.DetailView):
    model = WineListUpload
    template_name = "wine_wiki/winelistupload.html"


class WineListUploadCreateView(generic.CreateView):
    model = WineListUpload
    template_name = "wine_wiki/winelistupload_create.html"
    success_url = reverse_lazy("wine_wiki:wine-list-upload-list")
    form_class = WineListUploadForm


class WineListUploadDeleteView(generic.DeleteView):
    model = WineListUpload
    fields = ["name", "file"]
    template_name = "wine_wiki/winelistupload_delete.html"
    success_url = reverse_lazy("wine_wiki:wine-list-upload-list")


def winelistupload_ingestfromcsv(request):
    # TODO: add aggregation descriptors to top of wine list display page - number of wines, publication date, etc.
    if request.method == "POST":
        form = WineListRawIngestionForm(request.POST)
        if form.is_valid():
            pk = request.POST.get("winelistupload")
            wlu = WineListUpload.objects.get(pk=pk)
            csv_filepath = wlu.file.path

            if Path(csv_filepath).suffix != ".csv":
                raise ValueError("Expecting a csv file")

            # the WineListEdition parent table.
            with open(csv_filepath, "r") as f:
                reader = csv.DictReader(f)
                row_0 = next(reader)
                filepath = str(row_0["filepath"])
                pub_date = str(row_0["pub_date"])
                run_dt = str(row_0["run_dt"])

                wle = WineListEdition(
                    winelistupload=wlu,
                    filepath=filepath,
                    pub_date=pub_date,
                    run_dt=run_dt,
                )
                wle.save()

            with open(csv_filepath, "r") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    wlr = WineListRaw(
                        winelistedition=wle,
                        line_num_tot=row["line_num_tot"],
                        vintage=row["vintage"],
                        prod_wine_name=row["prod_wine_name"],
                        geo_int=row["geo_int"],
                        vol=row["vol"],
                        price=row["price"],
                        section_path=row["section_path"],
                        page_number=row["page_number"],
                        wine_type=row["wine_type"],
                        origin=row["origin"],
                        varietal=row["varietal"],
                    )
                    wlr.save()
                    wld = WineListDisplay(
                        line_num_tot=row["line_num_tot"],
                        vintage=row["vintage"],
                        prod_wine_name=row["prod_wine_name"],
                        geo_int=row["geo_int"],
                        vol=row["vol"],
                        price=row["price"],
                        section_path=row["section_path"],
                        page_number=row["page_number"],
                        wine_type=row["wine_type"],
                        origin=row["origin"],
                        varietal=row["varietal"],
                        winelistraw=wlr,
                    )
                    wld.save()

            return HttpResponseRedirect("/bennelong-wine-list/")
    else:
        form = WineListRawIngestionForm(request.POST)
    return render(request, "wine_wiki/winelistraw_create.html", {"form": form})
