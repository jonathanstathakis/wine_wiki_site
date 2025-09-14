import polars as pl


def select_wine_wiki_join_columns(wine_wiki, wine_wiki_join_columns):
    wine_wiki_join_fields = wine_wiki[wine_wiki_join_columns]
    return wine_wiki_join_fields


def extract_wine_wiki_join_strings(
    wine_wiki_join_fields, join_field_name="join_string"
):
    wine_wiki_strings = wine_wiki_join_fields.select(
        pl.concat_str(pl.all(), separator=" ", ignore_nulls=True).alias(join_field_name)
    )
    wine_wiki_string_list = wine_wiki_strings[join_field_name].to_list()

    return wine_wiki_string_list


def extract_wine_wiki_wine_from_db():
    with open("extract_wine_wiki_wine.sql", "r") as f:
        query = f.read()

    wine_wiki = pl.read_database_uri(query=query, uri="sqlite://db.sqlite3")

    return wine_wiki


def extract_wine_wiki():
    wine_wiki = extract_wine_wiki_wine_from_db()
    wine_wiki_join_columns = [
        "vintage",
        "base_year",
        "disgorg_year",
        "producer_name",
        "cuvee_name",
        "series",
        "vineyard",
        "commune",
        "wine_name",
        "classification",
    ]

    wine_wiki_join_fields = select_wine_wiki_join_columns(
        wine_wiki, wine_wiki_join_columns
    )
    wine_wiki_join_strings = extract_wine_wiki_join_strings(
        wine_wiki_join_fields=wine_wiki_join_fields
    )
    return wine_wiki_join_strings
