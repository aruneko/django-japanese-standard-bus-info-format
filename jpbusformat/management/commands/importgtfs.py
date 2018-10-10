from pathlib import Path

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("gtfs_name", metavar="GTFSが入っているディレクトリ名", type=str)

    def handle(self, *args, **options) -> None:
        gtfs_name = options.get("gtfs_name")

        file_list = list(Path(gtfs_name).glob("*.txt"))

        load_order = []

        object_cache = {}

        for cls in load_order:
            file_path = [f for f in file_list if f.name.endswith(cls._filename)]
            if file_path:
                cls.load_csv(file_path[0], object_cache)
                print(f"imported {cls._filename}")
            else:
                print(f"skip to import {cls._filename}")
                continue
