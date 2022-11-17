import h3
import pytest

from vehicle_location_service.gis_functions import report_new_location
from vehicle_location_service.models import Vehicle
from config import settings


@pytest.fixture
def populate_test_database(test_database):
    vehicles = [
        Vehicle(
            lat=lat,
            lng=lng,
            h3_cell=h3.geo_to_h3(lat, lng, settings.H3_RESOLUTION)
        )
        for lat, lng in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4))
    ]

    with test_database.atomic():
        Vehicle.bulk_create(vehicles)


def test_update_existing_vehicle(populate_test_database):
    updated_vehicle = report_new_location(1, 10, 10)

    assert updated_vehicle.lat == 10
    assert updated_vehicle.lng == 10
    assert updated_vehicle.h3_cell == "8858e06829fffff"


def test_cannot_update_non_existing_vehicle(populate_test_database):

    with pytest.raises(Vehicle.DoesNotExist):
        report_new_location(100, 10, 10)  # non-existing id
