from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Route(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="経路ID")
    agency = models.ForeignKey(
        "Agency", blank=True, null=True, on_delete=models.SET_NULL
    )
    short_name = models.CharField(max_length=256, help_text="経路略称")
    long_name = models.CharField(max_length=256, help_text="経路名")
    desc = models.CharField(max_length=256, blank=True, null=True, help_text="経路情報")
    type = models.IntegerField(
        choices=(
            (0, "Tram"),
            (1, "Subway"),
            (2, "Rail"),
            (3, "Bus"),
            (4, "Ferry"),
            (5, "Cable Car"),
            (6, "Gondola"),
            (7, "Funicular"),
        ),
        help_text="経路情報",
    )
    url = models.URLField(blank=True, null=True, help_text="経路URL")
    color = models.CharField(max_length=6, blank=True, null=True, help_text="経路色")
    text_color = models.CharField(
        max_length=6, blank=True, null=True, help_text="経路文字色"
    )
    sort_order = models.IntegerField(blank=True, null=True, help_text="表示順序")
    parent_route_id = models.CharField(
        max_length=256, blank=True, null=True, help_text="親路線ID"
    )

    class Meta:
        verbose_name_plural = "routes"

    _column_dict = {
        "route_id": "route_id",
        "agency_id": "agency_id",
        "route_short_name": "short_name",
        "route_long_name": "long_name",
        "route_desc": "desc",
        "route_type": "type",
        "route_url": "url",
        "route_color": "color",
        "route_text_color": "text_color",
        "route_sort_order": "sort_order",
        "jp_parent_route_id": "parent_route_id",
    }
    _filename = "routes.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        agencies = object_cache.get("agency") if object_cache.get("agency") else {}

        routes = [
            Route(
                route_id=d.get("route_id"),
                agency=agencies.get(d.get("agency_id")),
                short_name=d.get("short_name"),
                long_name=d.get("long_name"),
                desc=Converter(d.get("desc")).opt_str(),
                type=Converter(d.get("type")).to_int(),
                url=Converter(d.get("url")).opt_str(),
                color=Converter(d.get("color")).opt_str(),
                text_color=Converter(d.get("text_color")).opt_str(),
                sort_order=Converter(d.get("sort_order")).opt_int(),
                parent_route_id=Converter(d.get("parent_route_id")).opt_str(),
            )
            for d in csv_lines
        ]
        Route.objects.bulk_create(routes)

        object_cache["route"] = {}
        for route in routes:
            object_cache["route"][route.id] = route
