"""Parking floor entity class"""


class ParkingFloor:
    def __init__(self, floor_number, total_capacity) -> None:
        self.total_capacity = total_capacity
        self.floor_number = floor_number
        self.parking_spots = []  # list of parkingspot objects

    def add_parking_spot(self, parking_spot) -> bool:
        if len(self.parking_spots) < self.total_capacity:
            self.parking_spots.append(parking_spot)
            print(f"Slot {parking_spot} added to floor {self.floor_number}")
            return True
        print("Slot can'nt be added, floor capacity reached !")
        return False
