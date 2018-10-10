from pathlib import Path

from django.contrib.gis.db import models

from jpbusformat.utils import open_csv, Converter


class FeedInfo(models.Model):
    feed_publisher_name = models.CharField(max_length=256, help_text="提供組織名")
    feed_publisher_url = models.URLField(help_text="提供組織URL")
    feed_lang = models.CharField(max_length=2, help_text="提供言語")
    feed_start_date = models.DateField(blank=True, null=True, help_text="提供開始日")
    feed_end_date = models.DateField(blank=True, null=True, help_text="提供終了日")
    feed_version = models.CharField(
        max_length=256, blank=True, null=True, help_text="バージョン"
    )

    class Meta:
        verbose_name_plural = "feed_info"

    _column_dict = {
        "feed_publisher_name": "feed_publisher_name",
        "feed_publisher_url": "feed_publisher_url",
        "feed_lang": "feed_lang",
        "feed_start_date": "feed_start_date",
        "feed_end_date": "feed_end_date",
        "feed_version": "feed_version",
    }
    _filename = "feed_info.txt"

    @classmethod
    def load_csv(cls, file_path: Path, object_cache: dict) -> None:
        csv_lines = open_csv(file_path, cls._column_dict)

        feed_info = [
            FeedInfo(
                feed_publisher_name=d.get("feed_publisher_name"),
                feed_publisher_url=d.get("feed_publisher_url"),
                feed_lang=d.get("feed_lang"),
                feed_start_date=Converter(d.get("feed_start_date")).opt_date(),
                feed_end_date=Converter(d.get("feed_end_date")).opt_date(),
                feed_version=Converter(d.get("feed_version")).opt_str(),
            )
            for d in csv_lines
        ]
        FeedInfo.objects.bulk_create(feed_info)
