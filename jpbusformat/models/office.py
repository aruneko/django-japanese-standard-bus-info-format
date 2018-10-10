from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Office(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="営業所ID")
    name = models.CharField(max_length=256, help_text="営業所名")
    url = models.URLField(blank=True, null=True, help_text="営業所URL")
    phone = models.CharField(max_length=16, blank=True, null=True, help_text="営業所電話番号")

    _column_dict = {
        "office_id": "office_id",
        "office_name": "name",
        "office_url": "url",
        "office_phone": "phone",
    }
    _filename = "office_jp.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        offices = [
            Office(
                office_id=d.get("office_id"),
                name=d.get("name"),
                url=Converter(d.get("url")).opt_str(),
                phone=Converter(d.get("phone")).opt_str(),
            )
            for d in csv_lines
        ]
        Office.objects.bulk_create(offices)

        object_cache["office"] = {}
        for office in offices:
            object_cache["office"][office.id] = office
