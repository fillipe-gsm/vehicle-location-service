"""Entrypoint to expose the API endpoints"""
from bottle import Bottle, request

from vehicle_location_service.gis_functions import report_new_location


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

    return app
