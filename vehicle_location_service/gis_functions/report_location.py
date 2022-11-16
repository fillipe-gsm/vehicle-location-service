from pathlib import Path

from config import settings
from vehicle_location_service.data_types import Database, Vehicle


DATABASE_DEFAULT_PATH = Path().cwd() / settings.DATABASE_FILE


def report_new_location(
    vehicle_id: str,
    new_lat: float,
    new_lng: float,
    database_file_name: Path = DATABASE_DEFAULT_PATH,
) -> Vehicle:
    """Update location of a vehicle
    This function performs a GET-or-CREATE job: it updates the location of a
    current vehicle or create a new one if it does not exist yet.
    """

    import ipdb; ipdb.set_trace()
    database = Database.load(file_name=database_file_name)

    vehicle = database.vehicles_by_id.get(
        vehicle_id, Vehicle(vehicle_id=vehicle_id)
    )

    updated_vehicle = vehicle.copy(update={"lat": new_lat, "lng": new_lng})
    database.add(updated_vehicle, file_name=database_file_name)

    return updated_vehicle
