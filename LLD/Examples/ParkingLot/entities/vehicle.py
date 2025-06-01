"""entity class for vehicle"""


class VehicleType:
    TRUCK = "truck"
    CAR = "car"
    BIKE = "bike"


class Vehicle:
    def __init__(self, reg_number, vehicle_type: VehicleType) -> None:
        self.reg_number = reg_number
        self.vehicle_type = vehicle_type
