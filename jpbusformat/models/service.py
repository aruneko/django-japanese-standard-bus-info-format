from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Service(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="運行日ID")
    monday = models.BooleanField(help_text="月曜日の運行")
    tuesday = models.BooleanField(help_text="火曜日の運行")
    wednesday = models.BooleanField(help_text="水曜日の運行")
    thursday = models.BooleanField(help_text="木曜日の運行")
    friday = models.BooleanField(help_text="金曜日の運行")
    saturday = models.BooleanField(help_text="土曜日の運行")
    sunday = models.BooleanField(help_text="日曜日の運行")
    start_date = models.DateField(help_text="サービス開始日")
    end_date = models.DateField(help_text="サービス終了日")

    _column_dict = {
        "service_id": "service_id",
        "monday": "monday",
        "tuesday": "tuesday",
        "wednesday": "wednesday",
        "thursday": "thursday",
        "friday": "friday",
        "saturday": "saturday",
        "sunday": "sunday",
        "start_date": "start_date",
        "end_date": "end_date",
    }
    _filename = "calendar.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        services = [
            Service(
                service_id=d.get("service_id"),
                monday=Converter(d.get("monday")).to_bool(),
                tuesday=Converter(d.get("tuesday")).to_bool(),
                wednesday=Converter(d.get("wednesday")).to_bool(),
                thursday=Converter(d.get("thursday")).to_bool(),
                friday=Converter(d.get("friday")).to_bool(),
                saturday=Converter(d.get("saturday")).to_bool(),
                sunday=Converter(d.get("sunday")).to_bool(),
                start_date=Converter(d.get("start_date")).to_date(),
                end_date=Converter(d.get("end_date")).to_date(),
            )
            for d in csv_lines
        ]
        Service.objects.bulk_create(services)

        object_cache["service"] = {}
        for service in services:
            object_cache["service"][service.id] = service
