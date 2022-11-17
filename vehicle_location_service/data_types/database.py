import json
from pathlib import Path

from pydantic import BaseModel

from vehicle_location_service.data_types import Vehicle
from config import settings


DATABASE_PATH = Path().cwd() / settings.DATABASE_FILE


class Database(BaseModel):
    """Database implementation
    To simplify the problem and prevent relying on external database software,
    the actual database will be emulated via a JSON file in the format:
    {
        "1": vehicle_with_id_1_data,
        "2": vehicle_with_id_2_data,
        ...
    }

    wherein each vehicle data is provided via `Vehicle` class.
    """

    vehicles_by_id: dict[str, Vehicle]
    vehicles_id_by_h3_cell: dict[str, str] = {}

    def save(self) -> None:
        """Save data in a file"""
        with DATABASE_PATH.open("w", encoding="utf-8") as fb:
            json.dump(self.dict(), fb, indent=4)

    @classmethod
    def load(cls) -> "Database":
        """Load database from file"""
        with DATABASE_PATH.open("r", encoding="utf-8") as fb:
            json_data = json.load(fb)

        return cls(**json_data)

    def add(self, vehicle: Vehicle) -> None:
        """Add or update a vehicle in the database"""

        self.vehicles_by_id[vehicle.vehicle_id] = vehicle
        self.save()

    @property
    def vehicles(self) -> list[Vehicle]:
        """Return a list of all vehicles"""

        return list(self.vehicles_by_id.values())

    def _build_h3_lookup_table(self):
        """Build the vehicles look-up indexed by h3 cells"""
