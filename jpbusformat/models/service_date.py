from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class ServiceDate(models.Model):
    service = models.ForeignKey(
        "Service", related_name="service_dates", on_delete=models.CASCADE
    )
    date = models.DateField(help_text="日付")
    exception_type = models.IntegerField(
        choices=((1, "適用"), (2, "非適用")), help_text="運行区分"
    )

    _column_dict = {
        "service_id": "service_id",
        "date": "date",
        "exception_type": "exception_type",
    }
    _filename = "calendar_dates.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        services = object_cache["service"]

        service_dates = [
            ServiceDate(
                service=services[d.get("service_id")],
                date=Converter(d.get("date")).to_date(),
                exception_type=Converter(d.get("exception_type")).to_int(),
            )
            for d in csv_lines
        ]
        ServiceDate.objects.bulk_create(service_dates)
