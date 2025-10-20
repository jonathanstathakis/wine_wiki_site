from django.db import models
from wine_wiki.models import Wine, WineListDisplay


class FuzzyMatchListWiki(models.Model):
    wine_list = models.ForeignKey(to=WineListDisplay, on_delete=models.CASCADE)
    wine_list_query = models.CharField()
    wiki = models.ForeignKey(to=Wine, on_delete=models.CASCADE)
    wiki_choice = models.CharField()
    match_score = models.FloatField()
    review = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.wine_list} {self.wiki} {self.match_score}"
