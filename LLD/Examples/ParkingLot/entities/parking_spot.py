"""Parking slot entity class"""

from enum import Enum


class ParkingSpotType(Enum):
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"


class ParkingSpot:
    def __init__(self, spot_type: ParkingSpotType) -> None:
        self.spot_type = spot_type
        self.is_occupied = False
        self.occupied_by = None

    def park_vehicle(self, vehicle):
        if not self.is_occupied:
            self.is_occupied = True
            self.occupied_by = vehicle
            return True
        return False

    def unpark_vehicle(self):
        if self.is_occupied:
            self.is_occupied = False
            self.occupied_by = None
            return True
        return False
