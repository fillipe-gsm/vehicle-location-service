from pathlib import Path

from vehicle_location_service.data_types import Database, Vehicle


def report_new_location(
    vehicle_id: str,
    new_lat: float,
    new_lng: float,
) -> Vehicle:
    """Update location of a vehicle
    This function performs a GET-or-CREATE job: it updates the location of a
    current vehicle or create a new one if it does not exist yet.
    """

    database = Database.load()

    vehicle = database.vehicles_by_id.get(
        vehicle_id, Vehicle(vehicle_id=vehicle_id)
    )

    updated_vehicle = vehicle.copy(update={"lat": new_lat, "lng": new_lng})
    database.add(updated_vehicle)

    return updated_vehicle
