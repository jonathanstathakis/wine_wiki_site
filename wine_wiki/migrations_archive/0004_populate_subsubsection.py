# Generated by Django 5.2.4 on 2025-07-29 03:21

from django.db import migrations
import os
from pathlib import Path
import csv

from wine_wiki.models import SubSubSection


exported_data_path = Path(os.environ["WINE_LIST_DATA_DIR"])

subsubsection_path = exported_data_path / "subsubsection.csv"


def import_subsubsection(apps, schema_editor):
    SubSection = apps.get_model("wine_wiki", "SubSection")
    SubSubSection = apps.get_model("wine_wiki", "SubSubSection")
    Section = apps.get_model("wine_wiki", "Section")

    with open(subsubsection_path, "r") as f:
        csv_reader = csv.DictReader(f)

        for idx, row in [(idx, row) for idx, row in enumerate(csv_reader)]:
            # convert empty strings to nulls.
            cleaned_row = {k: (v if v != "" else None) for k, v in row.items()}
            section = Section.objects.get(section=cleaned_row.pop("section"))
            subsection = SubSection.objects.get(
                subsection=cleaned_row.pop("subsection")
            )

            subsubsection = SubSubSection(
                pk=cleaned_row["subsubsection_id"],
                section=section,
                subsection=subsection,
                order=cleaned_row["subsubsection_order"],
                subsubsection=cleaned_row["subsubsection"],
            )
            subsubsection.save()


def reverse_import_subsubsection(apps, schema_editor):
    """
    Get the rows corresponding to the input data and remove them.
    """
    SubSubSection = apps.get_model("wine_wiki", "SubSubSection")

    with open(subsubsection_path, "r") as f:
        csv_reader = csv.DictReader(f)

        for idx, row in [(idx, row) for idx, row in enumerate(csv_reader)]:
            cleaned_row = {k: (v if v != "" else None) for k, v in row.items()}
            section = cleaned_row["section"]
            subsection = cleaned_row["subsection"]
            subsubsection = cleaned_row["subsubsection"]

            SubSubSection.objects.get(
                section=section, subsection=subsection, subsubsection=subsubsection
            ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("wine_wiki", "0003_populate_subsection"),
    ]

    operations = []

    operations = [
        migrations.RunPython(
            code=import_subsubsection, reverse_code=reverse_import_subsubsection
        )
    ]
