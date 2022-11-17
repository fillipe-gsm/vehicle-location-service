from typing import Optional

import h3

from vehicle_location_service.models import Vehicle
from vehicle_location_service.data_types import Vehicle as VehicleSerializer
from config import settings


def report_new_location(
    new_lat: float,
    new_lng: float,
    vehicle_id: Optional[int] = None,
) -> VehicleSerializer:
    """Update location of a vehicle or create a new one

    Parameters
    ----------
    new_lat, new_lng
        Coordinates of the new location

    vehicle_id
        Id of the vehicle to be updated or `None` to create a new record

    Returns
    -------
    Updated vehicle

    Raises
    ------
    Vehicle.DoesNotExist if no vehicle matches `vehicle_id`
    """

    h3_cell = h3.geo_to_h3(new_lat, new_lng, settings.H3_RESOLUTION)

    updated_vehicle = (
        _update_existing_vehicle(new_lat, new_lng, vehicle_id, h3_cell)
        if vehicle_id
        else _create_new_vehicle(new_lat, new_lng, h3_cell)
    )

    return updated_vehicle.serialized


def _update_existing_vehicle(
    new_lat: float,
    new_lng: float,
    vehicle_id: int,
    h3_cell: str,
) -> Vehicle:
    """"""
    _ = (
        Vehicle.update(
            {
                Vehicle.lat: new_lat,
                Vehicle.lng: new_lng,
                Vehicle.h3_cell: h3_cell,
            }
        )
        .where(Vehicle.id == vehicle_id)
        .execute()
    )

    return Vehicle.get(Vehicle.id == vehicle_id)


def _create_new_vehicle(
    new_lat: float, new_lng: float, h3_cell: str
) -> Vehicle:
    """"""
    return Vehicle.create(lat=new_lat, lng=new_lng, h3_cell=h3_cell)
