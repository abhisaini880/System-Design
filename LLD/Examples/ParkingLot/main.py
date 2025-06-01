"""This is the controller file whihch will be used to interaact with parking components"""

from service.parking_service import ParkingService
from entities.parking_lot import ParkingLot
from entities.parking_spot import ParkingSpot, ParkingSpotType
from entities.parking_floor import ParkingFloor
from entities.vehicle import Vehicle, VehicleType
import time

spot1 = ParkingSpot(ParkingSpotType.LARGE)
floor1 = ParkingFloor(1, 10)
floor2 = ParkingFloor(2, 10)
lot1 = ParkingLot(2, "open_parking")

lot1.add_floor(floor1)
lot1.add_floor(floor2)

for spot_type in [
    ParkingSpotType.LARGE,
    ParkingSpotType.MEDIUM,
    ParkingSpotType.SMALL,
]:
    for _ in range(3):
        floor1.add_parking_spot(ParkingSpot(spot_type))
        floor2.add_parking_spot(ParkingSpot(spot_type))


parking_service = ParkingService(lot1)


v1 = Vehicle("HR01TY1101", VehicleType.CAR)
v2 = Vehicle("PB02TY1234", VehicleType.BIKE)
v3 = Vehicle("HR02TY3453", VehicleType.TRUCK)
v4 = Vehicle("UK01TY8657", VehicleType.CAR)
v5 = Vehicle("RJ01TY1234", VehicleType.BIKE)


t1 = parking_service.park_vehicle(v1)
t2 = parking_service.park_vehicle(v2)
t3 = parking_service.park_vehicle(v3)
t4 = parking_service.park_vehicle(v4)
t5 = parking_service.park_vehicle(v5)

time.sleep(3)
parking_service.unpark_vehicle(t1)
time.sleep(3)
parking_service.unpark_vehicle(t2)


print(t1, t2)
