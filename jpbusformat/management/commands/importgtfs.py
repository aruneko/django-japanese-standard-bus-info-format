from pathlib import Path

from django.core.management import BaseCommand

from jpbusformat.models.agency import Agency
from jpbusformat.models.agency_jp import AgencyJP
from jpbusformat.models.fare_attribute import FareAttribute
from jpbusformat.models.fare_rule import FareRule
from jpbusformat.models.feed_info import FeedInfo
from jpbusformat.models.frequency import Frequency
from jpbusformat.models.office import Office
from jpbusformat.models.route import Route
from jpbusformat.models.route_jp import RouteJP
from jpbusformat.models.service import Service
from jpbusformat.models.service_date import ServiceDate
from jpbusformat.models.shape import Shape
from jpbusformat.models.stop import Stop
from jpbusformat.models.stop_time import StopTime
from jpbusformat.models.transfer import Transfer
from jpbusformat.models.translation import Translation
from jpbusformat.models.trip import Trip


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("gtfs_name", metavar="GTFSが入っているディレクトリ名", type=str)

    def handle(self, *args, **options) -> None:
        gtfs_name = options.get("gtfs_name")

        file_list = list(Path(gtfs_name).glob("*.txt"))

        load_order = [
            Agency,
            AgencyJP,
            Stop,
            Route,
            RouteJP,
            Service,
            ServiceDate,
            Shape,
            Office,
            Trip,
            StopTime,
            FareAttribute,
            FareRule,
            Frequency,
            Transfer,
            FeedInfo,
            Translation,
        ]

        object_cache = {}

        for cls in load_order:
            file_path = [f for f in file_list if f.name.endswith(cls._filename)]
            if file_path:
                cls.load_csv(file_path[0], object_cache)
                print(f"imported {cls._filename}")
            else:
                print(f"skip to import {cls._filename}")
                continue
