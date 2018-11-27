from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Trip(models.Model):
    route = models.ForeignKey("Route", related_name="trips", on_delete=models.CASCADE)
    service = models.ForeignKey(
        "Service",
        related_name="trips",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    id = models.CharField(max_length=256, primary_key=True, help_text="便ID")
    headsign = models.CharField(max_length=256, blank=True, null=True, help_text="便行先")
    short_name = models.CharField(
        max_length=256, blank=True, null=True, help_text="便名称"
    )
    direction_id = models.IntegerField(
        choices=((0, "復路"), (1, "往路")), blank=True, null=True, help_text="上下区分"
    )
    block_id = models.CharField(
        max_length=256, blank=True, null=True, help_text="便結合区分"
    )
    shape = models.ForeignKey(
        "Shape", related_name="trips", on_delete=models.SET_NULL, blank=True, null=True
    )
    wheelchair_accessible = models.IntegerField(
        choices=((0, "不明"), (1, "利用可"), (2, "利用不可")),
        blank=True,
        null=True,
        help_text="車いす利用区分",
    )
    bikes_allowed = models.IntegerField(
        choices=((0, "不明"), (1, "利用可"), (2, "利用不可")),
        blank=True,
        null=True,
        help_text="自転車持込区分",
    )
    desc = models.CharField(max_length=256, blank=True, null=True, help_text="便情報")
    desc_symbol = models.CharField(
        max_length=16, blank=True, null=True, help_text="便記号"
    )
    office = models.ForeignKey(
        "Office", related_name="trips", on_delete=models.SET_NULL, blank=True, null=True
    )

    _column_dict = {
        "route_id": "route_id",
        "service_id": "service_id",
        "trip_id": "trip_id",
        "trip_headsign": "headsign",
        "trip_short_name": "short_name",
        "direction_id": "direction_id",
        "block_id": "block_id",
        "shape_id": "shape_id",
        "wheelchair_accessible": "wheelchair_accessible",
        "bikes_allowed": "bikes_allowed",
        "jp_trip_desc": "desc",
        "jp_trip_desc_symbol": "desc_symbol",
        "jp_office_id": "office_id",
    }
    _filename = "trips.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        routes = object_cache["route"]
        services = object_cache["service"]
        shapes = object_cache.get("shape") if object_cache.get("shape") else {}
        offices = object_cache.get("office") if object_cache.get("office") else {}

        trips = [
            Trip(
                route=routes[d.get("route_id")],
                service=services[d.get("service_id")],
                id=d.get("trip_id"),
                headsign=Converter(d.get("headsign")).opt_str(),
                short_name=Converter(d.get("short_name")).opt_str(),
                direction_id=Converter(d.get("direction_id")).opt_int(),
                block_id=Converter(d.get("block_id")).opt_str(),
                shape=shapes.get(Converter(d.get("shape_id")).opt_str()),
                wheelchair_accessible=Converter(
                    d.get("wheelchair_accessible")
                ).opt_int(),
                bikes_allowed=Converter(d.get("bikes_allowed")).opt_int(),
                desc=Converter(d.get("desc")).opt_str(),
                desc_symbol=Converter(d.get("desc_symbol")).opt_str(),
                office=offices.get(Converter(d.get("office_id")).opt_str()),
            )
            for d in csv_lines
        ]
        Trip.objects.bulk_create(trips)

        object_cache["trip"] = {}
        for trip in trips:
            object_cache["trip"][trip.id] = trip
