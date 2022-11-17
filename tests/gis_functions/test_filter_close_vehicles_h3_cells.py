import h3
import pytest

from vehicle_location_service.models import Vehicle
from vehicle_location_service.gis_functions import (
    filter_close_vehicles_h3_cells,
)
from config import settings


@pytest.fixture
def populate_test_database(test_database):
    vehicles = [
        Vehicle(
            lat=lat,
            lng=lng,
            h3_cell=h3.geo_to_h3(lat, lng, settings.H3_RESOLUTION),
        )
        for lat, lng in (
            (0, 0),
            (0.1, 0.1),
            (0.2, 0.2),
            (0.3, 0.3),
            (0.4, 0.4),
        )
    ]

    with test_database.atomic():
        Vehicle.bulk_create(vehicles)


def test_filter_close_vehicles_h3_cells_large_radius(populate_test_database):
    """With a large enough radius, all vehicles are selected"""
    close_vehicles = filter_close_vehicles_h3_cells(
        origin_lat=0.2,
        origin_lng=0.2,
        radius=50,
    )

    assert len(close_vehicles) == 5


def test_filter_close_vehicles_h3_cells_small_radius(populate_test_database):
    """
    In this case, only a vehicle in the same coordinate as the origin is within
    the desired radius
    """
    close_vehicles = filter_close_vehicles_h3_cells(
        origin_lat=0.2,
        origin_lng=0.2,
        radius=5,
    )

    assert len(close_vehicles) == 1


def test_no_close_vehicles(populate_test_database):
    """
    In a far origin there may be no close vehicles within the desired radius
    """
    close_vehicles = filter_close_vehicles_h3_cells(
        origin_lat=20,
        origin_lng=20,
        radius=100,
    )

    assert not close_vehicles
