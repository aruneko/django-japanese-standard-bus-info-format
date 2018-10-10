from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class StopTime(models.Model):
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    arrival_time = models.TimeField(help_text="到着時刻")
    departure_time = models.TimeField(help_text="出発時刻")
    stop = models.ForeignKey("Stop", on_delete=models.CASCADE)
    sequence = models.IntegerField(help_text="通過順序")
    headsign = models.CharField(
        max_length=256, blank=True, null=True, help_text="停留所行先"
    )
    pickup_type = models.IntegerField(
        choices=((0, "通常の乗車地"), (1, "乗車不可能"), (2, "交通機関へ要予約"), (3, "運転手へ要連絡")),
        blank=True,
        null=True,
        help_text="乗車区分",
    )
    drop_off_type = models.IntegerField(
        choices=((0, "通常の降車地"), (1, "降車不可能"), (2, "交通機関へ要予約"), (3, "運転手へ要連絡")),
        blank=True,
        null=True,
        help_text="降車区分",
    )
    shape_dist_traveled = models.FloatField(blank=True, null=True, help_text="通算距離")
    timepoint = models.IntegerField(
        choices=((0, "曖昧な時刻"), (1, "正確な時刻")), blank=True, null=True, help_text="発着時間精度"
    )

    _column_dict = {
        "trip_id": "trip_id",
        "arrival_time": "arrival_time",
        "departure_time": "departure_time",
        "stop_id": "stop_id",
        "stop_sequence": "sequence",
        "stop_headsign": "headsign",
        "pickup_type": "pickup_type",
        "drop_off_type": "drop_off_type",
        "shape_dist_traveled": "shape_dist_traveled",
        "timepoint": "timepoint",
    }
    _filename = "stop_times.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        trips = object_cache["trip"]
        stops = object_cache["stop"]

        stop_times = [
            StopTime(
                trip=trips[d.get("trip_id")],
                arrival_time=Converter(d.get("arrival_time")).to_time(),
                departure_time=Converter(d.get("departure_time")).to_time(),
                stop=stops[d.get("stop_id")],
                sequence=Converter(d.get("sequence")).to_int(),
                headsign=Converter(d.get("headsign")).opt_str(),
                pickup_type=Converter(d.get("pickup_type")).opt_int(),
                drop_off_type=Converter(d.get("drop_off_type")).opt_int(),
                shape_dist_traveled=Converter(d.get("shape_dist_traveled")).opt_float(),
                timepoint=Converter(d.get("timepoint")).opt_int(),
            )
            for d in csv_lines
        ]
        StopTime.objects.bulk_create(stop_times)
