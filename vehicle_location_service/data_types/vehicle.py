from pydantic import BaseModel


class Vehicle(BaseModel):
    """Schema for a vehicle and its properties

    Properties
    ----------
    id
        Identificator of a vehicle

    lat, lng
        Locations of last update

    h3_cell
        An string representation if its h3_cell in a specific resolution
        provided in the settings
    """

    id: int
    lat: float = 0
    lng: float = 0
    h3_cell: str = ""
