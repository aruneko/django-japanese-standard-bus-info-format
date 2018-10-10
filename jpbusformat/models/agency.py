from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import Converter, open_csv


class Agency(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="事業者法人番号")
    name = models.CharField(max_length=256, help_text="事業者名称")
    url = models.URLField(help_text="事業者URL")
    timezone = models.CharField(max_length=32, help_text="タイムゾーン")
    lang = models.CharField(max_length=8, blank=True, null=True, help_text="言語")
    phone = models.CharField(max_length=16, blank=True, null=True, help_text="電話番号")
    fare_url = models.URLField(blank=True, null=True, help_text="オンライン購入URL")
    email = models.EmailField(blank=True, null=True, help_text="事業者Eメール")

    class Meta:
        verbose_name_plural = "agencies"

    _column_dict = {
        "agency_id": "id",
        "agency_name": "name",
        "agency_url": "url",
        "agency_timezone": "timezone",
        "agency_lang": "lang",
        "agency_phone": "phone",
        "agency_fare_url": "fare_url",
        "agency_email": "email",
    }
    _filename = "agency.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)
        agencies = [
            Agency(
                agency_id=d.get("id"),
                name=d.get("name"),
                url=d.get("url"),
                timezone=d.get("timezone"),
                lang=Converter(d.get("lang")).opt_str(),
                phone=Converter(d.get("phone")).opt_str(),
                fare_url=Converter(d.get("fare_url")).opt_str(),
                email=Converter(d.get("email")).opt_str(),
            )
            for d in csv_lines
        ]
        Agency.objects.bulk_create(agencies)

        object_cache["agency"] = {}
        for agency in agencies:
            object_cache["agency"][agency.id] = agency
