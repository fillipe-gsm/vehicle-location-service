from pathlib import Path

import pytest

from vehicle_location_service.data_types import Database, Vehicle

@pytest.fixture
def database_file_name(tmp_path):
    return tmp_path / "test_database.json"


@pytest.fixture
def vehicles_by_id():
    return {
        "0": Vehicle(vehicle_id="0", lat=0, lng=0),
        "1": Vehicle(vehicle_id="1", lat=1, lng=1),
        "2": Vehicle(vehicle_id="2", lat=2, lng=2),
        "3": Vehicle(vehicle_id="3", lat=3, lng=3),
        "4": Vehicle(vehicle_id="4", lat=4, lng=4),
    }


def test_can_save_database(vehicles_by_id, database_file_name):
    """Check if database file is properly created"""
    # Given
    database = Database(vehicles_by_id=vehicles_by_id)

    # When
    database.save(file_name=database_file_name)

    # Then
    assert database_file_name.exists()


def test_can_load_database():
    # Test database with 5 vehicles
    database_file_name = Path().cwd() / "tests/data/test_database.json"

    database = Database.load(file_name=database_file_name)

    assert len(database.vehicles_by_id) == 5
