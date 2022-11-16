from pathlib import Path

import pytest

from vehicle_location_service.gis_functions import filter_close_vehicles


@pytest.fixture
def database_file_name():
    return Path().cwd() / "tests/data/test_database.json"


def test_filter_close_vehicles_large_radius(database_file_name):
    """With a large enough radius, all vehicles are selected"""
    close_vehicles = filter_close_vehicles(
        origin_lat=2,
        origin_lng=2,
        radius=500,
        database_file_name=database_file_name,
    )

    assert len(close_vehicles) == 5


def test_filter_close_vehicles_small_radius(database_file_name):
    """
    In this case, only a vehicle in the same coordinate as the origin is within
    the desired radius
    """
    close_vehicles = filter_close_vehicles(
        origin_lat=2,
        origin_lng=2,
        radius=5,
        database_file_name=database_file_name,
    )

    assert len(close_vehicles) == 1


def test_no_close_vehicles(database_file_name):
    """
    In a far origin there may be no close vehicles within the desired radius
    """
    close_vehicles = filter_close_vehicles(
        origin_lat=20,
        origin_lng=20,
        radius=100,
        database_file_name=database_file_name,
    )

    assert not close_vehicles
