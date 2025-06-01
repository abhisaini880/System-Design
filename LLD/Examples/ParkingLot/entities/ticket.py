"""Entity class for Ticket"""

import time


class Ticket:
    def __init__(self, vehicle, parking_spot):
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.in_time = time.time()
        self.out_time = None

    def calculate_fee(self):
        pass

    def _set_out_time(self):
        pass

    def __repr__(self) -> str:
        return f"Ticket for {self.vehicle.reg_number} with in time: {self.in_time} and out_time: {self.out_time}"
