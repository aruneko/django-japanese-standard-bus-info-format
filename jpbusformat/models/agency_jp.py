from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class AgencyJP(models.Model):
    agency = models.OneToOneField(
        "Agency", on_delete=models.CASCADE, related_name="agency"
    )
    official_name = models.CharField(
        max_length=256, blank=True, null=True, help_text="事業者正式名称"
    )
    zip_number = models.CharField(
        max_length=256, blank=True, null=True, help_text="事業者郵便番号"
    )
    address = models.CharField(max_length=256, blank=True, null=True, help_text="事業者住所")
    president_pos = models.CharField(
        max_length=256, blank=True, null=True, help_text="代表者肩書"
    )
    president_name = models.CharField(
        max_length=256, blank=True, null=True, help_text="代表者氏名"
    )

    class Meta:
        verbose_name_plural = "agencies_jp"

    _column_dict = {
        "agency_id": "id",
        "agency_official_name": "official_name",
        "agency_zip_number": "zip_number",
        "agency_address": "address",
        "agency_president_pos": "president_pos",
        "agency_president_name": "president_name",
    }
    _filename = "agency_jp.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        agencies = object_cache["agency"]

        agencies = [
            AgencyJP(
                agency=agencies.get(d.get("id")),
                official_name=Converter(d.get("official_name")).opt_str(),
                zip_number=Converter(d.get("zip_number")).opt_str(),
                address=Converter(d.get("address")).opt_str(),
                president_pos=Converter(d.get("president_pos")).opt_str(),
                president_name=Converter(d.get("president_name")).opt_str(),
            )
            for d in csv_lines
        ]
        AgencyJP.objects.bulk_create(agencies)
