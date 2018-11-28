from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv


class Translation(models.Model):
    trans_id = models.CharField(max_length=256, help_text="翻訳元日本語")
    lang = models.CharField(max_length=8, help_text="言語")
    translation = models.CharField(max_length=256, help_text="翻訳先言語")

    _column_dict = {
        "trans_id": "trans_id",
        "lang": "lang",
        "translation": "translation",
    }
    _filename = "translations.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        translations = [
            Translation(
                trans_id=d.get("trans_id"),
                lang=d.get("lang"),
                translation=d.get("translation"),
            )
            for d in csv_lines
        ]
        Translation.objects.bulk_create(translations)
