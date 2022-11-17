"""Entrypoint to expose the API endpoints"""
from typing import Any

from bottle import Bottle, request, response

from vehicle_location_service.models import Vehicle
from vehicle_location_service.gis_functions import (
    report_new_location,
    filter_close_vehicles,
    filter_close_vehicles_h3_cells,
)


def create_app() -> Bottle:
    """Create the WSGI app to be run in a server"""

    app = Bottle()

    @app.post("/vehicle")
    def add_vehicle_location() -> dict[str, Any]:
        new_lat = float(request.json["lat"])
        new_lng = float(request.json["lng"])

        updated_vehicle = report_new_location(
            new_lat=new_lat,
            new_lng=new_lng,
        ).dict()

        return {"vehicle": updated_vehicle}

    @app.put("/vehicle")
    def update_vehicle_location() -> dict[str, Any]:
        vehicle_id = int(request.json["vehicle_id"])
        new_lat = float(request.json["lat"])
        new_lng = float(request.json["lng"])

        try:
            updated_vehicle = report_new_location(
                new_lat=new_lat,
                new_lng=new_lng,
                vehicle_id=vehicle_id,
            ).dict()
        except Vehicle.DoesNotExist:
            updated_vehicle = None
            response.status = 404

        return {"vehicle": updated_vehicle}

    @app.get("/closest-vehicles")
    def closest_vehicles() -> dict[str, Any]:
        origin_lat = float(request.query.get("origin_lat"))
        origin_lng = float(request.query.get("origin_lng"))
        radius = float(request.query.get("radius"))
        method = request.query.get("method", "h3-cells")

        if method == "h3-cells":
            closest_vehicles = filter_close_vehicles_h3_cells(
                origin_lat, origin_lng, radius
            )
        else:
            closest_vehicles = filter_close_vehicles(
                origin_lat, origin_lng, radius
            )

        closest_vehicles_json = [
            vehicle.dict() for vehicle in closest_vehicles
        ]

        return {"closest_vehicles": closest_vehicles_json}

    return app
