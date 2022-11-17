import h3
import numpy as np

from vehicle_location_service.models import Vehicle
from vehicle_location_service.data_types import Vehicle as VehicleSerializer
from vehicle_location_service.distances import great_circle_distance_matrix
from config import settings


def filter_close_vehicles_h3_cells(
    origin_lat: float,
    origin_lng: float,
    radius: float,
) -> list[VehicleSerializer]:
    """Filter vehicles within a radius `radius` from a given origin
    Instead of looping through all vehicles in the database to compute their
    distances, a pre-processing is applied. The idea is to find all H3 cells
    containing the radius, and filter only the vehicles inside them.

    Notes
    -----
    Here are the steps:
    1. Find the corresponding cell of the incoming origin. Since the cells are
    small enough, we can assume the cell center is a good approximation for the
    actual location;
    2. Convert the radius in km into grid distance by diving it with the
    average edge length of the cell
        2.5. We overestimate the actual grid distance by one more unit to
        account for the fact that the `k_ring` method is approximate
    3. Find all cells contained in this radius
    4. Filter all vehicles with an h3 cell contained in the list returned
    before. Since they are indexed this lookup should be pretty fast
    5. Compute the distance from the origin with this (hopefully) reduced set
    """
    vehicles = _filter_vehicles_inside_ring_cells(
        origin_lat, origin_lng, radius
    )

    if not vehicles:
        return []

    vehicle_coordinates = np.array(
        [(vehicle.lat, vehicle.lng) for vehicle in vehicles]
    )
    origin = np.array([(origin_lat, origin_lng)])
    distance_matrix = great_circle_distance_matrix(origin, vehicle_coordinates)
    close_vehicles_mask = (distance_matrix <= radius).squeeze(axis=0)

    return [
        vehicle.serialized
        for i, vehicle in enumerate(vehicles)
        if close_vehicles_mask[i]
    ]


def _filter_vehicles_inside_ring_cells(
    origin_lat: float,
    origin_lng: float,
    radius: float,
) -> list[Vehicle]:
    origin_h3_cell = h3.geo_to_h3(
        origin_lat, origin_lng, settings.H3_RESOLUTION
    )

    cell_length = h3.edge_length(settings.H3_RESOLUTION, unit="km")
    k_neighborhood_size = 1 + round(radius / cell_length)

    ring_cells = h3.k_ring(origin_h3_cell, k=k_neighborhood_size)

    return Vehicle.select().where(Vehicle.h3_cell.in_(ring_cells))
