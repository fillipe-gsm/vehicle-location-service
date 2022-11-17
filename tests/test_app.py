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
            h3_cell=h3.geo_to_h3(lat, lng, settings.H3_RESOLUTION),
        )
        for lat, lng in ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4))
    ]

    with test_database.atomic():
        Vehicle.bulk_create(vehicles)


@pytest.fixture
def client_app():
    app = create_app()

    return TestApp(app)


class TestReportVehicleLocation:
    def test_add_new_vehicle(self, client_app, populate_test_database):
        database_len = Vehicle.select().count()

        response = client_app.post_json(
            "/vehicle", params={"lat": 10, "lng": 10}
        )

        assert response.status_code == 200
        assert Vehicle.select().count() == database_len + 1

    def test_report_vehicle_location_existing_vehicle(
        self, client_app, populate_test_database
    ):
        response = client_app.put_json(
            "/vehicle", params={"vehicle_id": 1, "lat": 10, "lng": 10}
        )

        expected_response = {
            "vehicle": {
                "id": 1,
                "lat": 10,
                "lng": 10,
                "h3_cell": h3.geo_to_h3(10, 10, settings.H3_RESOLUTION),
            }
        }

        assert response.json == expected_response
        assert response.status_code == 200

    def test_report_vehicle_location_nonexisting_vehicle(
        self, client_app, populate_test_database
    ):
        """We should get a status 404 and an empty output"""
        with pytest.raises(AppError):
            client_app.put_json(
                "/vehicle", params={"vehicle_id": -1, "lat": 10, "lng": 10}
            )


@pytest.mark.parametrize("method", ["regular", "h3-cells"])
def test_get_closest_vehicles(client_app, populate_test_database, method):
    response = client_app.get(
        "/closest-vehicles",
        params={
            "origin_lat": 2,
            "origin_lng": 2,
            "radius": 5,
            "method": method,
        },
    )

    expected_response = {
        "closest_vehicles": [
            {
                "id": 3,
                "lat": 2,
                "lng": 2,
                "h3_cell": h3.geo_to_h3(2, 2, settings.H3_RESOLUTION),
            }
        ]
    }

    assert response.json == expected_response
