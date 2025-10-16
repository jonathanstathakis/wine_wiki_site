from . import models
from django.db import connection


def load_autofilleditions(wle_left, wle_right):
    """
    generate new autofillrun and insert selected editions into
    autofilleditions
    """

    afr = models.AutoFillRun()
    afr.save()
    afe = models.AutoFillEditions(
        autofillrun=afr, edition_left=wle_left, edition_right=wle_right
    )
    afe.save()


def run_self_join_query(edition_left_id, edition_right_id):
    """
    fill 'pending' table with left and right edition wine
    identified where right edition has a wine key.
    """
    from wine_wiki_site.settings import BASE_DIR
    from pathlib import Path

    query_fp = (
        Path(BASE_DIR) / "wine_wiki" / "table_match_autofill" / "wld_selfjoin.sql"
    )

    with open(query_fp, "r") as f:
        query = f.read()

    with connection.cursor() as cursor:
        for statement in query.split(";"):
            cursor.execute(statement)
    # afp = models.AutoFillPending.objects.all()


def load_autofillpending(wl_editions):
    """ """

    wl_editions["edition_left_id"]
    edition_left_id = wl_editions["edition_left_id"]
    edition_right_id = wl_editions["edition_right_id"]

    autofillpending = run_self_join_query(
        edition_left_id=edition_left_id, edition_right_id=edition_right_id
    )
