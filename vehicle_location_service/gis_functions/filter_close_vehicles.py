from pathlib import Path

import numpy as np

from vehicle_location_service.data_types import Database, Vehicle
from vehicle_location_service.distances import great_circle_distance_matrix
from config import settings


DATABASE_DEFAULT_PATH = Path().cwd() / settings.DATABASE_FILE


def filter_close_vehicles(
    origin_lat: float,
    origin_lng: float,
    radius: float,
    database_file_name: Path = DATABASE_DEFAULT_PATH,
) -> list[Vehicle]:
    """Filter all vehicles within ``radius`` from an origin location

    Parameters
    ----------
    origin_lat, origin_lng
        Coordinates of the origin point

    radius
        Radius delimiting the desired region in km

    Returns
    -------
    List of vehicles within a Great Circle distance of the desired radius
    from the origin point
    """

    database = Database.load(file_name=database_file_name)

    vehicle_coordinates = np.array(
        [(vehicle.lat, vehicle.lng) for vehicle in database.vehicles]
    )
    origin = np.array([(origin_lat, origin_lng)])
    distance_matrix = great_circle_distance_matrix(origin, vehicle_coordinates)
    close_vehicles_mask = (distance_matrix <= radius).squeeze()

    return [
        vehicle for i, vehicle in enumerate(database.vehicles)
        if close_vehicles_mask[i]
    ]
