from vehicle_location_service.database import database
from vehicle_location_service.models import Vehicle


if __name__ == "__main__":
    database.create_tables([Vehicle])
