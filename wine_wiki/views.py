from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Producer, Wine, Variety
from collections import defaultdict
from django.urls import reverse, reverse_lazy
from .forms import UserRegisterForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
# Create your views here.


class WineView(generic.DetailView):
    model = Wine
    template_name = "wine_wiki/wine.html"
    context_object_name = "wine"

    def get_context_data(self, **kwargs):
        context = super(WineView, self).get_context_data(**kwargs)

        wine = context["wine"]

        title_fields = [
            wine.vintage,
            wine.producer,
            wine.cuvee_name,
            wine.variety,
        ]

        context["wine_title"] = ", ".join(
            [str(x) for x in title_fields if x is not None]
        )

        return context


class WineListView(generic.ListView):
    model = Wine
    template_name = "wine_wiki/wine_list.html"
    context_object_name = "wine_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wine_list = (
            Wine.objects.all()
            .select_related("section", "subsection", "producer", "variety")
            .order_by("section__order", "subsection__order", "line_num_tot")
        )

        grouped = defaultdict(lambda: defaultdict(list))

        for wine in wine_list:
            grouped[wine.section][wine.subsection].append(wine)

        # have to pass a dict to context rather than defaultdict
        context["grouped_wines"] = {
            str(k): {str(u): w for u, w in v.items()} for k, v in grouped.items()
        }
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
