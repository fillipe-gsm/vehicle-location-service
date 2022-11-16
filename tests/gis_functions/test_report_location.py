from pathlib import Path

import pytest

from vehicle_location_service.gis_functions import report_new_location
from vehicle_location_service.data_types import Database, Vehicle


@pytest.fixture
def database_file_name(tmp_path):
    return tmp_path / "test_database.json"


@pytest.fixture
def populate_test_database(database_file_name):
    vehicles_by_id = {
        "0": Vehicle(vehicle_id="0", lat=0, lng=0),
        "1": Vehicle(vehicle_id="1", lat=1, lng=1),
        "2": Vehicle(vehicle_id="2", lat=2, lng=2),
        "3": Vehicle(vehicle_id="3", lat=3, lng=3),
        "4": Vehicle(vehicle_id="4", lat=4, lng=4),
    }

    database = Database(vehicles_by_id=vehicles_by_id)
    database.save(file_name=database_file_name)


@pytest.mark.parametrize("vehicle_id", ["0", "10"])
def test_update_vehicle(
    database_file_name, populate_test_database, vehicle_id
):
    """Id "0" represents an existing vehicle and "10" is from a new one
    In both cases the data should be properly updated
    """
    # Given
    expected_updated_vehicle = Vehicle(vehicle_id=vehicle_id, lat=10, lng=10)

    # When
    updated_vehicle = report_new_location(
        vehicle_id, 10, 10, database_file_name=database_file_name
    )

    # Then
    database = Database.load(file_name=database_file_name)
    updated_vehicle_on_database = database.vehicles_by_id[vehicle_id]

    # Check the database was updated and it returned the updated vehicle
    assert updated_vehicle == expected_updated_vehicle
    assert updated_vehicle_on_database == expected_updated_vehicle
