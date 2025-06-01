"""Entity class for parking lot"""


class ParkingLot:
    def __init__(self, floor_capacity, name) -> None:
        self.floor_capacity = floor_capacity
        self.name = name
        self.floors = {}

    def add_floor(self, parking_floor):
        if len(self.floors) < self.floor_capacity:
            self.floors.update({parking_floor: parking_floor.total_capacity})
            print(
                f"Parking floor: {parking_floor} added to parking lot : {self.name}!"
            )
            return True
        print(f"Max floor limit reached for parking lot : {self.name}")
        return False
