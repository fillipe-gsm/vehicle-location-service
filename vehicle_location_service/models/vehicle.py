import peewee as pw

from vehicle_location_service.database import database
from vehicle_location_service.data_types import Vehicle as VehicleSerializer


class Vehicle(pw.Model):
    lat = pw.FloatField(default=0)
    lng = pw.FloatField(default=0)
    h3_cell = pw.CharField(default="", index=True)

    class Meta:
        database = database

    @property
    def serialized(self) -> VehicleSerializer:
        """Return a serializable version of the object"""
        return VehicleSerializer(
            id=self.id,
            lat=self.lat,
            lng=self.lng,
            h3_cell=self.h3_cell,
        )
