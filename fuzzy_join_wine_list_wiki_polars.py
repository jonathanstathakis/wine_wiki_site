import polars as pl
from pathlib import Path

from extract_wine_wiki import extract_wine_wiki
from extract_wine_list import extract_wine_list


def main():
    pl.Config(tbl_width_chars=1000, fmt_str_lengths=1000)

    wine_list_join_strings = extract_wine_list()
    wine_wiki_join_strings = extract_wine_wiki()

    assert wine_wiki_join_strings
    assert wine_list_join_strings


if __name__ == "__main__":
    main()
