import h3

from vehicle_location_service.models import Vehicle
from vehicle_location_service.data_types import Vehicle as VehicleSerializer
from config import settings


def report_new_location(
    vehicle_id: int,
    new_lat: float,
    new_lng: float,
) -> VehicleSerializer:
    """Update location of a vehicle

    Parameters
    ----------
    vehicle_id
        Id of the vehicle to be updated

    new_lat, new_lng
        Coordinates of the new location

    Returns
    -------
    Updated vehicle

    Raises
    ------
    Vehicle.DoesNotExist if no vehicle matches `vehicle_id`
    """

    h3_cell = h3.geo_to_h3(new_lat, new_lng, settings.H3_RESOLUTION)
    _ = (
        Vehicle
        .update(
            {
                Vehicle.lat: new_lat,
                Vehicle.lng: new_lng,
                Vehicle.h3_cell: h3_cell
            }
        )
        .where(Vehicle.id == vehicle_id)
        .execute()
    )

    updated_vehicle = Vehicle.get(Vehicle.id == vehicle_id)

    return updated_vehicle.serialized
