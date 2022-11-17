from webtest import TestApp, AppError
import pytest
import h3

from vehicle_location_service.app import create_app
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


@pytest.fixture
def client_app():
    app = create_app()

    return TestApp(app)


def test_report_vehicle_location(
    client_app, populate_test_database
):
    response = client_app.post_json(
        "/vehicle", params={"vehicle_id": 1, "lat": 10, "lng": 10}
    )

    expected_response = {
        "vehicle": {
            "id": 1, "lat": 10, "lng": 10, "h3_cell": "8858e06829fffff"
        }
    }

    assert response.json == expected_response
    assert response.status_code == 200


def test_report_vehicle_location_nonexisting_vehicle(
    client_app, populate_test_database
):
    """We should get a status 404 and an empty output"""
    with pytest.raises(AppError):
        client_app.post_json(
            "/vehicle", params={"vehicle_id": -1, "lat": 10, "lng": 10}
        )


def test_get_closest_vehicles(
    client_app, populate_test_database
):
    response = client_app.get(
        "/closest-vehicles",
        params={"origin_lat": 2, "origin_lng": 2, "radius": 5},
    )

    expected_response = {
        "closest_vehicles": [
            {"id": 3, "lat": 2, "lng": 2, "h3_cell": "88756e44adfffff"}
        ]
    }

    assert response.json == expected_response
