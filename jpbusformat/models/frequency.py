from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Frequency(models.Model):
    trip = models.OneToOneField("Trip", related_name="trip", on_delete=models.CASCADE)
    start_time = models.TimeField(help_text="開始時刻")
    end_time = models.TimeField(help_text="終了時刻")
    headway_secs = models.IntegerField(help_text="運行間隔")
    exact_times = models.IntegerField(
        choices=((0, "不正確"), (1, "正確")), blank=True, null=True, help_text="案内精度"
    )

    class Meta:
        verbose_name_plural = "frequencies"

    _column_dict = {
        "trip_id": "trip_id",
        "start_time": "start_time",
        "end_time": "end_time",
        "headway_secs": "headway_secs",
        "exact_times": "exact_times",
    }
    _filename = "frequencies.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        trips = object_cache["trip"]

        frequencies = [
            Frequency(
                trip=trips[d.get("trip_id")],
                start_time=Converter(d.get("start_time")).to_time(),
                end_time=Converter(d.get("end_time")).to_time(),
                headway_secs=Converter(d.get("headway_secs")).to_int(),
                exact_times=Converter(d.get("exact_times")).opt_int(),
            )
            for d in csv_lines
        ]
        Frequency.objects.bulk_create(frequencies)
