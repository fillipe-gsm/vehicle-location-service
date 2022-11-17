import h3

from vehicle_location_service.models import Vehicle
from config import settings


NUM_VEHICLES = 10_000
SCALE_FACTOR = 1000


def populate_table():
    vehicles = [
        Vehicle(
            lat=num / SCALE_FACTOR,
            lng=num / SCALE_FACTOR,
            h3_cell=h3.geo_to_h3(
                num / SCALE_FACTOR,
                num / SCALE_FACTOR,
                settings.H3_RESOLUTION,
            ),
        )
        for num in range(NUM_VEHICLES)
    ]

    Vehicle.bulk_create(vehicles)


if __name__ == "__main__":
    populate_table()
