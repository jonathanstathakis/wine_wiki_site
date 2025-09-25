from .models import (
    FuzzyMatchListWiki,
    WineListDisplay,
    Wine,
    WineListEdition,
)
from rapidfuzz import process


import logging

logger = logging.getLogger(__name__)


def run_fuzzy_match(queries: list[str], choices: list[str]):
    """
    The actual match process. Need to get the left and right strings,
    calculate their match, save the results to the results model for downtrack review.
    """
    from rapidfuzz import process

    results = []

    for i, query in enumerate(queries):
        choice, score, idx = process.extractOne(query, choices=choices)
        results.append((i, idx, score))

    return results


def get_wine_list_not_joined(wle) -> list[tuple[int, str, str, str]]:
    """
    get all WineListDisplay objects not joined to a Wine
    """

    logger.info("extracting wine list wines not matched to a wiki wine..")

    list_value_fields = ["vintage", "prod_wine_name", "geo_int", "section_path"]

    # need to get latest wine list edition.
    # randomise order to try and break up continuously incorrect matches
    # over multiple runs
    wine_list = WineListDisplay.objects.filter(
        winelistraw__winelistedition=wle, wine_id=None
    ).order_by("?")
    wine_list_values = list(wine_list.values_list("id", *list_value_fields))

    # section_path is a heirarchy from section to subsubsection whose meaning
    # is different depending on the section. Simplest approach is to inject it
    # into the query by replacing the '/' with a space.
    section_path_idx = 4

    for idx, wine in enumerate(wine_list_values):
        section_path = wine[section_path_idx]
        new_section_path = section_path.replace("/", " ")
        new_wine = list(wine)
        new_wine[4] = new_section_path
        wine_list_values[idx] = tuple(new_wine)

    return wine_list_values


def get_wiki_not_joined() -> list[tuple[int, str]]:
    logger.info("extracting wiki wines not linked to a wine list wine.")

    identifier_fields = [
        "vintage",
        "base_year",
        "disgorg_year",
        "producer__name",
        "cuvee_name",
        "series",
        "vineyard",
        "commune",
        "wine_name",
        "classification",
        "region",
        "subregion",
        "style",
        "variety__name",
    ]

    not_joined_wines = Wine.objects.filter(winelistdisplay__isnull=True).order_by("?")
    wiki = not_joined_wines.values_list("id", *identifier_fields)

    return wiki


def form_match_strings(wiki):
    match_strings = []

    for row in wiki:
        match_string = " ".join([str(x).lower() for x in row[1:] if x])

        match_strings.append({"id": row[0], "match_string": match_string})

    return match_strings


def load_results(results):
    """
    load results into table
    """

    logger.info("loading fuzzy match results into db..")

    for row in results:
        fmlw = FuzzyMatchListWiki(
            wine_list=WineListDisplay.objects.get(id=row["wine_list_id"]),
            wine_list_query=row["wine_list_query"],
            wiki=Wine.objects.get(id=row["wiki_choice_id"]),
            wiki_choice=row["wiki_choice"],
            match_score=round(row["match_score"], 2),
        )
        fmlw.save()


def fuzzy_match_list_wiki(wle):
    """
    2 step fuzzy match where subsets are formed first based on matching
    of producer.

    Do the first then the second as the second requires more
    refactoring.
    """
    wine_list = get_wine_list_not_joined(wle=wle)
    wiki = get_wiki_not_joined()
    wiki_match_strings = form_match_strings(wiki)
    list_match_strings = form_match_strings(wine_list)

    results = []

    choices = [row["match_string"] for row in wiki_match_strings]
    logger.info("beginning fuzzy match.")

    for row in list_match_strings:
        if len(choices) > 0:
            choice, score, choice_idx = process.extractOne(
                row["match_string"], choices=choices
            )

            ## assumes unique entries.
            choice_id = [
                wr["id"] for wr in wiki_match_strings if wr["match_string"] == choice
            ][0]

            choices.pop(choice_idx)

            results.append(
                {
                    "wine_list_id": row["id"],
                    "wine_list_query": row["match_string"],
                    "wiki_choice": choice,
                    "wiki_choice_id": choice_id,
                    "match_score": score,
                }
            )

        else:
            results.append(
                {
                    "wine_list_id": row[0],
                    "wine_list_query": row[1],
                    "wiki_choice": "no more choices available",
                    "wiki_choice_id": "",
                    "match_score": "",
                }
            )
    load_results(results)

    logger.info("fuzzy match complete.")
