from django.contrib.gis import admin

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
from jpbusformat.models.zone import Zone

admin.site.register(Agency, admin.GeoModelAdmin)
admin.site.register(AgencyJP, admin.GeoModelAdmin)
admin.site.register(FareAttribute, admin.GeoModelAdmin)
admin.site.register(FareRule, admin.GeoModelAdmin)
admin.site.register(FeedInfo, admin.GeoModelAdmin)
admin.site.register(Frequency, admin.GeoModelAdmin)
admin.site.register(Office, admin.GeoModelAdmin)
admin.site.register(Route, admin.GeoModelAdmin)
admin.site.register(RouteJP, admin.GeoModelAdmin)
admin.site.register(Service, admin.GeoModelAdmin)
admin.site.register(ServiceDate, admin.GeoModelAdmin)
admin.site.register(Shape, admin.GeoModelAdmin)
admin.site.register(Stop, admin.GeoModelAdmin)
admin.site.register(StopTime, admin.GeoModelAdmin)
admin.site.register(Transfer, admin.GeoModelAdmin)
admin.site.register(Translation, admin.GeoModelAdmin)
admin.site.register(Trip, admin.GeoModelAdmin)
admin.site.register(Zone, admin.GeoModelAdmin)
