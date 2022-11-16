from pathlib import Path

import pytest

from vehicle_location_service.gis_functions import report_location
from vehicle_location_service.data_types import Database, Vehicle


@pytest.mark.parametrize("vehicle_id", ["0", "10"])
def test_update_vehicle(vehicle_id):
    """Id "0" represents an existing vehicle and "10" is from a new one
    In both cases the data should be properly updated
    """
    # Given
    database_file_name = Path().cwd() / "tests/data/test_database.json"
    expected_updated_vehicle = Vehicle(vehicle_id=vehicle_id, lat=10, lng=10)

    # When
    updated_vehicle = report_location(
        vehicle_id, 10, 10, database_file_name=database_file_name
    )

    # Then
    database = Database.load(file_name=database_file_name)
    updated_vehicle_on_database = database.vehicles_by_id[vehicle_id]

    # Check the database was updated and it returned the updated vehicle
    assert updated_vehicle == expected_updated_vehicle
    assert updated_vehicle_on_database == expected_updated_vehicle
