import polars as pl


def select_wine_list_join_columns(wine_list, wine_list_join_columns):
    wine_list_join_fields = wine_list[wine_list_join_columns]
    return wine_list_join_fields


def extract_wine_list_join_strings(
    wine_list_join_fields, join_field_name="join_string"
):
    """ """

    wine_list_strings = wine_list_join_fields.select(
        pl.concat_str(pl.all(), separator=" ").alias(join_field_name)
    )

    wine_list_string_list = wine_list_strings["join_string"].to_list()

    return wine_list_string_list


def select_wine_list_section(wine_list: pl.DataFrame):
    filtered_wine_list = wine_list.filter(
        ~pl.col("section_path").str.contains("Sparkling")
    )

    return filtered_wine_list


def extract_wine_list():
    wine_list = pl.read_csv("wine_list.csv")
    wine_list_join_columns = [
        "vintage",
        "prod_wine_name",
        "geo_int",
    ]
    filtered_wine_list = select_wine_list_section(wine_list)
    wine_list_join_fields = select_wine_list_join_columns(
        wine_list=filtered_wine_list, wine_list_join_columns=wine_list_join_columns
    )
    wine_list_join_strings = extract_wine_list_join_strings(wine_list_join_fields)
    return wine_list_join_strings
