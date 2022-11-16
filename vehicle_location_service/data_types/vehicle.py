from pydantic import BaseModel


class Vehicle(BaseModel):
    """Schema for a vehicle and its attributes"""

    vehicle_id: str
    lat: float = 0
    lng: float = 0
