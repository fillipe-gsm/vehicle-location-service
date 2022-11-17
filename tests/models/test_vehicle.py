from vehicle_location_service.models import Vehicle
from vehicle_location_service.data_types import Vehicle as VehicleSerializer


def test_serialize_vehicle(test_database):
    vehicle = Vehicle.create(lat=0, lng=0, h3_cell="abcd")

    expected_vehicle_serialized = VehicleSerializer(
        id=1, lat=0, lng=0, h3_cell="abcd"
    )

    vehicle.serialized == expected_vehicle_serialized
