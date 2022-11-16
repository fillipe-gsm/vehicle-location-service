"""Entrypoint to expose the API endpoints"""
from bottle import Bottle, request

from vehicle_location_service.gis_functions import (
    report_new_location, filter_close_vehicles
)


def create_app() -> Bottle:
    """Create the WSGI app to be run in a server"""

    app = Bottle()

    @app.post("/vehicle")
    def vehicle_location():
        vehicle_id = request.json["vehicle_id"]
        new_lat = request.json["lat"]
        new_lng = request.json["lng"]

        updated_vehicle = report_new_location(vehicle_id, new_lat, new_lng)

        return {"vehicle": updated_vehicle.dict()}

    @app.get("/closest-vehicles")
    def closest_vehicles():
        origin_lat = float(request.query.get("origin_lat"))
        origin_lng = float(request.query.get("origin_lng"))
        radius = float(request.query.get("radius"))

        closest_vehicles = filter_close_vehicles(
            origin_lat, origin_lng, radius
        )

        closest_vehicles_json = [
            vehicle.dict() for vehicle in closest_vehicles
        ]

        return {"closest_vehicles": closest_vehicles_json}

    return app
