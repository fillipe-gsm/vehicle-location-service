from webtest import TestApp
from mock import patch
import pytest

from vehicle_location_service.app import create_app
from vehicle_location_service.data_types import Database, Vehicle


@pytest.fixture
def client_app():
    app = create_app()

    return TestApp(app)


@pytest.fixture
def database_file_name(tmp_path):
    return tmp_path / "test_database.json"


@pytest.fixture
def mocked_database_path(database_file_name):
    with patch(
        "vehicle_location_service.data_types.database.DATABASE_PATH",
        database_file_name,
    ) as mocked_path:
        yield mocked_path


@pytest.fixture
def populate_test_database(mocked_database_path):
    vehicles_by_id = {
        "0": Vehicle(vehicle_id="0", lat=0, lng=0),
        "1": Vehicle(vehicle_id="1", lat=1, lng=1),
        "2": Vehicle(vehicle_id="2", lat=2, lng=2),
        "3": Vehicle(vehicle_id="3", lat=3, lng=3),
        "4": Vehicle(vehicle_id="4", lat=4, lng=4),
    }

    database = Database(vehicles_by_id=vehicles_by_id)
    database.save()


def test_report_vehicle_location(
    client_app, populate_test_database, mocked_database_path
):
    response = client_app.post_json(
        "/vehicle", params={"vehicle_id": "0", "lat": 10, "lng": 10}
    )

    expected_response = {"vehicle": {"vehicle_id": "0", "lat": 10, "lng": 10}}

    assert response.json == expected_response


def test_get_closest_vehicles(
    client_app, populate_test_database, mocked_database_path
):
    response = client_app.get(
        "/closest-vehicles",
        params={"origin_lat": 2, "origin_lng": 2, "radius": 5},
    )

    expected_response = {
        "closest_vehicles": [{"vehicle_id": "2", "lat": 2, "lng": 2}]
    }

    assert response.json == expected_response
