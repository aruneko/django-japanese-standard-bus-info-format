from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class Transfer(models.Model):
    from_stop = models.ForeignKey(
        "Stop", on_delete=models.CASCADE, related_name="from_stops", help_text="乗継元標柱"
    )
    to_stop = models.ForeignKey(
        "Stop", on_delete=models.CASCADE, related_name="to_stops", help_text="乗継先標柱"
    )
    transfer_type = models.IntegerField(
        choices=((0, "推奨乗継地点"), (1, "時間考慮済み乗継地点"), (2, "乗継時間指定"), (3, "乗継不可能")),
        help_text="乗継タイプ",
    )
    min_transfer_time = models.IntegerField(blank=True, null=True, help_text="乗継時間")

    _column_dict = {
        "from_stop_id": "from_stop_id",
        "to_stop_id": "to_stop_id",
        "transfer_type": "transfer_type",
        "min_transfer_time": "min_transfer_time",
    }
    _filename = "transfers.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        stops = object_cache["stop"]

        transfers = [
            Transfer(
                from_stop=stops[d.get("from_stop_id")],
                to_stop=stops[d.get("to_stop_id")],
                transfer_type=Converter(d.get("transfer_type")).to_int(),
                min_transfer_time=Converter(d.get("min_transfer_time")).opt_int(),
            )
            for d in csv_lines
        ]
        Transfer.objects.bulk_create(transfers)
