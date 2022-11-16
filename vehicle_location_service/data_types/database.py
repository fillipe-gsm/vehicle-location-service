import json
from pathlib import Path, PosixPath

from pydantic import BaseModel

from vehicle_location_service.data_types import Vehicle


DATABASE_DEFAULT_PATH = Path().cwd() / "data/database.json"


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

    def save(self, file_name: PosixPath = DATABASE_DEFAULT_PATH) -> None:
        """Save data in a file"""
        with file_name.open("w", encoding="utf-8") as fb:
            json.dump(self.dict(), fb, indent=4)

    @classmethod
    def load(cls, file_name: PosixPath = DATABASE_DEFAULT_PATH) -> "Database":
        """Load database from file"""
        with file_name.open("r", encoding="utf-8") as fb:
            json_data = json.load(fb)

        return cls(**json_data)
