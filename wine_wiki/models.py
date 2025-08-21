from django.contrib.admin import display
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import default, slugify
from django.utils.translation import autoreload_started
from django.urls import reverse
from taggit.managers import TaggableManager


class Producer(models.Model):
    """represents a producer"""

    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField(
        help_text="Description of the producer", default="", blank=True
    )

    def get_absolute_url(self):
        return reverse("wine_wiki:producer", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("region", "name")


class Variety(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(
        help_text="Description of the variety", default="", blank=True
    )

    def get_absolute_url(self):
        return reverse("wine_wiki:variety", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("name",)


class Section(models.Model):
    """
    Represents the wine list structure
    """

    order = models.IntegerField(unique=True)
    section = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return str(self.section)


class SubSection(models.Model):
    """
    mixin class for wine list subcategories
    """

    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    subsection = models.CharField(max_length=100, primary_key=True)
    order = models.IntegerField()

    def __str__(self):
        return str(self.subsection)


class SubSubSection(models.Model):
    """
    mixin class for wine list subcategories
    """

    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    subsection = models.ForeignKey(SubSection, on_delete=models.PROTECT)
    subsubsection = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.section=} {self.subsubsection=} {self.subsubsection=}"


class Wine(models.Model):
    """base class representing a wine object"""

    # wine-list-etl fields
    merged_text_ext = models.TextField(
        blank=True,
        null=True,
        default=None,
    )  # left over from field extractoin, also here for debugging
    merged_text = models.TextField(
        blank=True,
        null=True,
        default=None,
    )  # the initial extracted text, useful for downstream debugging

    # bpos fields
    bpos_key = models.CharField(max_length=100, blank=True, null=True, default=None)

    # remaining fields
    vintage = models.CharField(max_length=4, blank=True, null=True, default=None)
    base_year = models.IntegerField(
        blank=True,
        null=True,
        default=None,
    )
    cuvee_name = models.TextField(blank=True, null=True, default=None)
    disgorg_year = models.IntegerField(blank=True, null=True, default=None)
    price = models.IntegerField(blank=True, default=0)
    producer = models.ForeignKey(to=Producer, null=True, on_delete=models.PROTECT)
    dryness = models.CharField(max_length=100, blank=True, null=True, default=None)
    country = models.CharField(max_length=100, blank=True, null=True, default=None)
    state = models.CharField(max_length=100, blank=True, null=True, default=None)
    region = models.CharField(max_length=100, blank=True, null=True, default=None)
    subregion = models.CharField(max_length=100, blank=True, null=True, default=None)
    commune = models.CharField(max_length=100, blank=True, null=True, default=None)
    vineyard = models.CharField(max_length=100, blank=True, null=True, default=None)
    wine_name = models.CharField(max_length=100, blank=True, null=True, default=None)
    variety = models.ForeignKey(to=Variety, default="", on_delete=models.PROTECT)
    style = models.CharField(max_length=100, blank=True, null=True, default=None)
    classification = models.CharField(
        max_length=100, blank=True, null=True, default=None
    )
    volume = models.CharField(max_length=100, blank=True, null=True, default=None)
    series = models.CharField(max_length=100, blank=True, null=True, default=None)
    description = models.TextField(
        blank=True,
        null=True,
        default=None,
        help_text="All unstructured information about the wine. Supports Markdown formatting (see <a href=https://www.markdownguide.org/>guide</a>). Description is a 2nd level header field within the page, try to use third level and lower if including headers.",
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )  # date added to website database

    modification_on = models.DateTimeField(
        auto_now=True
    )  # date added to website database

    # add modifier name
    # update wines with already existing descriptions to map the author to the description

    last_modification_by = models.CharField(max_length=50, null=True)

    tags = TaggableManager(blank=True)

    def get_absolute_url(self):
        return reverse("wine_wiki:wine", kwargs={"pk": self.pk})

    def __str__(self):
        disp_str = ", ".join(
            filter(
                None,
                [
                    str(self.vintage),
                    str(self.producer),
                    self.cuvee_name,
                    str(self.variety),
                    self.subregion,
                    self.region,
                    self.state,
                ],
            )
        )
        return disp_str

    def winesearcher_str(self):
        """assemble a string that matches winesearcher"""
        return f"{self.producer} {self.wine_name} {self.variety} {self.subregion} {self.region}/{self.vintage}".replace(
            " ", "+"
        ).replace("++", "+")  # in the event of null fields

    def search_eng_str(self):
        """assemble a string that matches winesearcher"""
        return f"{self.producer} {self.wine_name} {self.variety} {self.subregion} {self.region} {self.vintage}".replace(
            " ", "+"
        ).replace("++", "+")  # in the event of null fields

    def wine_title(self):
        title_fields = [
            self.vintage,
            self.producer,
            self.cuvee_name,
            self.variety,
        ]

        wine_title = ", ".join([str(x) for x in title_fields if x is not None])
        return wine_title


class BennelongWineList(models.Model):
    """Bennelong wine list data"""

    line_num_tot = models.IntegerField(
        null=True, default=-1
    )  # -1 implies missing number, can apply a default sort by name in view
    page_num = models.IntegerField(null=False, default=-1)
    page_line_num = models.IntegerField(null=False, default=-1)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, null=True)
    subsection = models.ForeignKey(SubSection, on_delete=models.PROTECT, null=True)
    subsubsection = models.CharField(default="")
    wine = models.ForeignKey(to=Wine, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ("section__order", "subsection__order", "line_num_tot")

    def __str__(self):
        return f"{self.line_num_tot=}, {self.page_num=}, {self.section.section=}, {self.subsection.subsection=}, {self.subsubsection=}, {self.wine.__str__()=}"
