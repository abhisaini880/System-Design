"""Parking Service that will be managing the parking lot"""

from entities.vehicle import Vehicle, VehicleType
from entities.parking_spot import ParkingSpotType
from entities.ticket import Ticket
from typing import Optional
import time

VEHICLE_PARKING_SPOT_MAPPING = {
    VehicleType.TRUCK: ParkingSpotType.LARGE,
    VehicleType.CAR: ParkingSpotType.MEDIUM,
    VehicleType.BIKE: ParkingSpotType.SMALL,
}


class ParkingService:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def park_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        required_parking_spot = VEHICLE_PARKING_SPOT_MAPPING[
            vehicle.vehicle_type
        ]

        for parking_floor in self.parking_lot.floors:
            for parking_spot in parking_floor.parking_spots:
                if (
                    parking_spot.spot_type == required_parking_spot
                    and not parking_spot.is_occupied
                ):
                    if not parking_spot.park_vehicle(vehicle):
                        continue
                    ticket = Ticket(vehicle, parking_spot)
                    return ticket

        return None

    def unpark_vehicle(self, ticket):
        parking_spot = ticket.parking_spot
        if parking_spot and parking_spot.occupied_by == ticket.vehicle:
            parking_spot.unpark_vehicle()
            out_time = time.time()
            ticket.out_time = out_time
            print(
                f"Vehicle unparked and billed for time: {(out_time-ticket.in_time)}s "
            )
