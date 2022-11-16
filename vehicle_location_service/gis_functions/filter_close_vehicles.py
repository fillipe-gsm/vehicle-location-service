from pathlib import Path

import numpy as np

from vehicle_location_service.data_types import Database, Vehicle
from vehicle_location_service.distances import great_circle_distance_matrix


def filter_close_vehicles(
    origin_lat: float,
    origin_lng: float,
    radius: float,
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

    database = Database.load()

    vehicle_coordinates = np.array(
        [(vehicle.lat, vehicle.lng) for vehicle in database.vehicles]
    )
    origin = np.array([(origin_lat, origin_lng)])
    distance_matrix = great_circle_distance_matrix(origin, vehicle_coordinates)
    close_vehicles_mask = (distance_matrix <= radius).squeeze()

    return [
        vehicle
        for i, vehicle in enumerate(database.vehicles)
        if close_vehicles_mask[i]
    ]
