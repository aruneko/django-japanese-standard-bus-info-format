from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class FareAttribute(models.Model):
    id = models.CharField(max_length=256, primary_key=True, help_text="運賃ID")
    price = models.IntegerField(help_text="運賃")
    currency_type = models.CharField(max_length=3, help_text="通貨")
    payment_method = models.IntegerField(
        choices=((0, "後払い"), (1, "前払い")), help_text="支払いタイミング"
    )
    transfers = models.IntegerField(
        choices=((0, "不可"), (1, "1度だけ可"), (2, "2度だけ可")), help_text="乗換"
    )
    agency = models.ForeignKey(
        "Agency",
        related_name="fare_attributes",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    transfer_duration = models.IntegerField(blank=True, null=True, help_text="乗換有効秒数")

    _column_dict = {
        "fare_id": "id",
        "price": "price",
        "currency_type": "currency_type",
        "payment_method": "payment_method",
        "transfers": "transfers",
        "agency_id": "agency",
        "transfer_duration": "transfer_duration",
    }
    _filename = "fare_attributes.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        agencies = object_cache["agency"]

        fare_attributes = [
            FareAttribute(
                id=d.get("id"),
                price=Converter(d.get("price")).to_int(),
                currency_type=d.get("currency_type"),
                payment_method=Converter(d.get("payment_method")).to_int(),
                transfers=Converter(d.get("transfers")).to_int(),
                agency=agencies.get(Converter(d.get("agency")).opt_str()),
                transfer_duration=Converter(d.get("transfer_duration")).opt_int(),
            )
            for d in csv_lines
        ]
        FareAttribute.objects.bulk_create(fare_attributes)

        object_cache["fare"] = {}
        for fare_attribute in fare_attributes:
            object_cache["fare"][fare_attribute.id] = fare_attribute
