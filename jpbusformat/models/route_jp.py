from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class RouteJP(models.Model):
    route = models.OneToOneField(
        "Route", on_delete=models.CASCADE, related_name="route"
    )
    update_date = models.DateField(blank=True, null=True, help_text="ダイヤ改正日")
    origin_stop = models.CharField(
        max_length=256, blank=True, null=True, help_text="起点"
    )
    via_stop = models.CharField(max_length=256, blank=True, null=True, help_text="経由地")
    destination_stop = models.CharField(
        max_length=256, blank=True, null=True, help_text="終点"
    )

    class Meta:
        verbose_name_plural = "routes_jp"

    _column_dict = {
        "route_id": "route_id",
        "route_update_date": "update_date",
        "origin_stop": "origin_stop",
        "via_stop": "via_stop",
        "destination_stop": "destination_stop",
    }
    _filename = "routes_jp.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        route_caches = object_cache["route"]

        routes = [
            RouteJP(
                route=route_caches[d.get("route_id")],
                update_date=Converter(d.get("update_date")).opt_date(),
                origin_stop=Converter(d.get("origin_stop")).opt_str(),
                via_stop=Converter(d.get("via_stop")).opt_str(),
                destination_stop=Converter(d.get("destination_stop")).opt_str(),
            )
            for d in csv_lines
        ]
        RouteJP.objects.bulk_create(routes)
