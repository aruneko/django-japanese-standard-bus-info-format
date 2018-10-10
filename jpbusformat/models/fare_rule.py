from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class FareRule(models.Model):
    fare = models.ForeignKey("FareAttribute", on_delete=models.CASCADE)
    route = models.ForeignKey("Route", on_delete=models.CASCADE)
    origin = models.ForeignKey(
        "Zone",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="乗車地ゾーン",
        related_name="origin_zones",
    )
    destination = models.ForeignKey(
        "Zone",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="降車地ゾーン",
        related_name="destination_zones",
    )
    contains = models.ForeignKey(
        "Zone",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="通過ゾーン",
        related_name="contains_zones",
    )

    _column_dict = {
        "fare_id": "fare_id",
        "route_id": "route_id",
        "origin_id": "origin_id",
        "destination_id": "destination_id",
        "contains_id": "destination_id",
    }
    _filename = "fare_rules.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        fare_attributes = object_cache["fare"]
        routes = object_cache["route"]
        zones = object_cache.get("zone") if object_cache.get("zone") else {}

        fare_rules = [
            FareRule(
                fare=fare_attributes[d.get("fare_id")],
                route=routes[d.get("route_id")],
                origin=zones.get(Converter(d.get("origin_id")).opt_str()),
                destination=zones.get(Converter(d.get("destination_id")).opt_str()),
                contains=zones.get(Converter(d.get("contains_id")).opt_str()),
            )
            for d in csv_lines
        ]
        FareRule.objects.bulk_create(fare_rules)
