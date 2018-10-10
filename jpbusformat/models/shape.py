from itertools import groupby
from pathlib import Path

from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString, Point

from jpbusformat.utils import open_csv, Converter


def _create_point(d: dict) -> Point:
    return Point(x=Converter(d["lon"]).to_float(), y=Converter(d["lat"]).to_float())


class Shape(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="描画ID")
    line = models.LineStringField(help_text="バス路線形状")

    _column_dict = {
        "shape_id": "shape_id",
        "shape_pt_lat": "lat",
        "shape_pt_lon": "lon",
        "shape_pt_sequence": "sequence",
        "shape_dist_traveled": "dist_traveled",
    }

    _filename = "shapes.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        grouped_lines = groupby(csv_lines, key=lambda d: d["shape_id"])
        shapes = [
            Shape(
                id=k,
                line=LineString(
                    [
                        _create_point(l)
                        for l in sorted(lines, key=lambda p: p["sequence"])
                    ]
                ),
            )
            for k, lines in grouped_lines
        ]
        Shape.objects.bulk_create(shapes)

        object_cache["shape"] = {}
        for shape in shapes:
            object_cache["shape"][shape.id] = shape
