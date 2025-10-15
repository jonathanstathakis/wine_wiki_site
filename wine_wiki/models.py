from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
import time

epoch_start = time.gmtime(0)


class Producer(models.Model):
    """represents a producer"""

    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100, default="", blank=True)
    description = models.TextField(
        help_text="Description of the producer", default="", blank=True
    )

    def get_absolute_url(self):
        return reverse("wine_wiki:producer", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("region", "name")

    def __str__(self):
        return str(self.name)


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

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subsection = models.CharField(max_length=100, primary_key=True)
    order = models.IntegerField()

    def __str__(self):
        return str(self.subsection)


class SubSubSection(models.Model):
    """
    mixin class for wine list subcategories
    """

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE)
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

    def field_names(self) -> list[str]:
        return [
            "vintage",
            "base_year",
            "disgorg_year",
            "producer_id",
            "cuvee_name",
            "dryness",
            "country",
            "state",
            "region",
            "subregion",
            "commune",
            "vineyard",
            "wine_name",
            "variety_id",
            "style",
            "classification",
            "series",
            "volume",
        ]

    def wine_title(self):
        title_fields = [
            self.vintage,
            self.producer.name,
            self.series,
            self.cuvee_name,
            self.wine_name,
            self.variety,
            self.region,
            self.subregion,
            self.commune,
            self.vineyard,
            self.style,
            self.classification,
            self.volume,
        ]

        wine_title = ", ".join(
            [str(x) for x in title_fields if (x is not None and x != "")]
        )
        return wine_title

    def wine_fields(self):
        """print all user-relevant fields of the wine"""
        fields = {k: v for k, v in self.__dict__.items() if k in self.field_names()}
        return fields


class WineListUpload(models.Model):
    file = models.FileField(upload_to="wine_list/")
    name = models.CharField(unique=True)
    dt_upload = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("wine_wiki:wine-list-upload", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


class WineListEdition(models.Model):
    """
    parent table of the wines in WineListRaw and WineListDisplay. Stores information
    such as publication date and other metadata.
    """

    winelistupload = models.ForeignKey(to=WineListUpload, on_delete=models.CASCADE)
    filepath = models.CharField(default="")
    pub_date = models.DateTimeField(unique=True)
    run_dt = models.DateTimeField()

    def __str__(self):
        return str(f"Published: {self.pub_date.strftime('%Y/%m/%d')}")


class WineListRaw(models.Model):
    """
    the raw data from the ETL.

    Kept distinct from the Display data as the raw fields are used for linking
    bennelong the output of the ETL to the Wine and Display models.
    """

    winelistedition = models.ForeignKey(to=WineListEdition, on_delete=models.CASCADE)
    line_num_tot = models.IntegerField()
    vintage = models.CharField(default="")
    prod_wine_name = models.CharField(default="")
    geo_int = models.CharField(default="")
    vol = models.CharField(default="")
    price = models.IntegerField(default=-1)
    section_path = models.CharField(default="")
    page_number = models.IntegerField()
    wine_type = models.CharField(default="")
    origin = models.CharField(default="")
    varietal = models.CharField(default="")


class WineListDisplay(models.Model):
    """Bennelong wine list data"""

    wine = models.ForeignKey(to=Wine, on_delete=models.CASCADE, null=True)
    winelistraw = models.ForeignKey(to=WineListRaw, on_delete=models.CASCADE)
    line_num_tot = models.IntegerField(default=-1)
    vintage = models.CharField(default="")
    prod_wine_name = models.CharField(default="")
    geo_int = models.CharField(default="")
    vol = models.CharField(default="")
    price = models.IntegerField(default=-1)
    section_path = models.CharField(default="")
    page_number = models.IntegerField(default=-1)
    wine_type = models.CharField(default="")
    origin = models.CharField(default="")
    varietal = models.CharField(default="")

    def field_names(self):
        return [
            "wine",
            "winelistraw",
            "line_num_tot",
            "vintage",
            "prod_wine_name",
            "geo_int",
            "vol",
            "price",
            "section_path",
            "page_number",
            "wine_type",
            "origin",
            "varietal",
        ]

    def fields(self):
        return {k: v for k, v in self.__dict__.items() if k in self.field_names()}

    def __str__(self):
        return f"{self.line_num_tot} {self.vintage} {self.prod_wine_name} {self.geo_int} {self.vol} {self.price} {self.page_number} {self.wine_type} {self.origin} {self.varietal}"


class FuzzyMatchListWiki(models.Model):
    wine_list = models.ForeignKey(to=WineListDisplay, on_delete=models.CASCADE)
    wine_list_query = models.CharField()
    wiki = models.ForeignKey(to=Wine, on_delete=models.CASCADE)
    wiki_choice = models.CharField()
    match_score = models.FloatField()
    review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.wine_list} {self.wiki} {self.match_score}"
