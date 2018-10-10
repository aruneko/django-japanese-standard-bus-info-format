from __future__ import annotations
from pathlib import Path

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from jpbusformat.models.zone import Zone
from jpbusformat.utils import open_csv, Converter


class Stop(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="停留所・標柱ID")
    code = models.CharField(max_length=256, blank=True, null=True, help_text="停留所・標柱番号")
    name = models.CharField(max_length=256, help_text="停留所・標柱名称")
    desc = models.CharField(
        max_length=256, blank=True, null=True, help_text="停留所・標柱付加情報"
    )
    point = models.PointField(help_text="座標")
    zone = models.ForeignKey("Zone", blank=True, null=True, on_delete=models.SET_NULL)
    url = models.URLField(blank=True, null=True, help_text="停留所・標柱URL")
    location_type = models.IntegerField(
        blank=True, null=True, choices=((0, "標柱"), (1, "停留所")), help_text="停留所・標柱区分"
    )
    parent_station = models.ForeignKey(
        "Stop", blank=True, null=True, on_delete=models.SET_NULL
    )
    timezone = models.CharField(
        max_length=32, blank=True, null=True, help_text="タイムゾーン"
    )
    wheelchair_boarding = models.IntegerField(
        blank=True,
        null=True,
        choices=((0, "不明"), (1, "利用可"), (2, "利用不可")),
        help_text="車椅子情報",
    )

    _column_dict = {
        "stop_id": "stop_id",
        "stop_code": "code",
        "stop_name": "name",
        "stop_desc": "desc",
        "stop_lat": "lat",
        "stop_lon": "lon",
        "zone_id": "zone_id",
        "stop_url": "url",
        "location_type": "location_type",
        "parent_station": "parent_station_id",
        "stop_timezone": "timezone",
        "wheelchair_boarding": "wheelchair_boarding",
    }
    _filename = "stops.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        zones = [Zone(id=d["zone_id"]) for d in csv_lines if d["zone_id"]]
        Zone.objects.bulk_create(zones)

        object_cache["zone"] = {}

        for zone in zones:
            object_cache["zone"][zone.id] = zone

        parent_stops = [
            Stop(
                stop_id=d.get("stop_id"),
                code=Converter(d.get("code")).opt_str(),
                name=d.get("name"),
                desc=Converter(d.get("desc")).opt_str(),
                point=Point(
                    Converter(d.get("lon")).to_float(),
                    Converter(d.get("lat")).to_float(),
                ),
                zone=object_cache["zone"].get(Converter(d.get("zone_id")).opt_str()),
                url=Converter(d.get("url")).opt_str(),
                location_type=Converter(d.get("location_type")).opt_int(),
                timezone=Converter(d.get("timezone")).opt_str(),
                wheelchair_boarding=Converter(d.get("wheelchair_boarding")).opt_int(),
            )
            for d in csv_lines
            if d["location_type"] == "1"
        ]
        Stop.objects.bulk_create(parent_stops)

        object_cache["stop"] = {}

        for stop in parent_stops:
            object_cache["stop"][stop.id] = stop

        stops = [
            Stop(
                stop_id=d.get("stop_id"),
                code=Converter(d.get("code")).opt_str(),
                name=d.get("name"),
                desc=Converter(d.get("desc")).opt_str(),
                point=Point(
                    Converter(d.get("lon")).to_float(),
                    Converter(d.get("lat")).to_float(),
                ),
                zone=object_cache["zone"].get(Converter(d.get("zone_id")).opt_str()),
                url=Converter(d.get("url")).opt_str(),
                location_type=Converter(d.get("location_type")).opt_int(),
                parent_station=object_cache["stop"].get(
                    Converter(d.get("parent_station_id")).opt_str()
                ),
                timezone=Converter(d.get("timezone")).opt_str(),
                wheelchair_boarding=Converter(d.get("wheelchair_boarding")).opt_int(),
            )
            for d in csv_lines
            if d["location_type"] == "0"
        ]
        Stop.objects.bulk_create(stops)

        for stop in stops:
            object_cache["stop"][stop.id] = stop
