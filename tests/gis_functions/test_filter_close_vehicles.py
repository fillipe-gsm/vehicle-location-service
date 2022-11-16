from pathlib import Path

import pytest
from mock import patch

from vehicle_location_service.gis_functions import filter_close_vehicles


@pytest.fixture
def database_file_name():
    return Path().cwd() / "tests/data/test_database.json"


@pytest.fixture
def mocked_database_path(database_file_name):
    with patch(
        "vehicle_location_service.data_types.database.DATABASE_PATH",
        database_file_name
    ) as mocked_path:
        yield mocked_path


def test_filter_close_vehicles_large_radius(mocked_database_path):
    """With a large enough radius, all vehicles are selected"""
    close_vehicles = filter_close_vehicles(
        origin_lat=2,
        origin_lng=2,
        radius=500,
    )

    assert len(close_vehicles) == 5


def test_filter_close_vehicles_small_radius(mocked_database_path):
    """
    In this case, only a vehicle in the same coordinate as the origin is within
    the desired radius
    """
    close_vehicles = filter_close_vehicles(
        origin_lat=2,
        origin_lng=2,
        radius=5,
    )

    assert len(close_vehicles) == 1


def test_no_close_vehicles(mocked_database_path):
    """
    In a far origin there may be no close vehicles within the desired radius
    """
    close_vehicles = filter_close_vehicles(
        origin_lat=20,
        origin_lng=20,
        radius=100,
    )

    assert not close_vehicles
