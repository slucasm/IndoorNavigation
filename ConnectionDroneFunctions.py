from pymavlink import *
from dronekit import connect



def droneConnection():
    connection_string = '/dev/serial0'
    connection_baudrate = 921600

    try:
        vehicle = connect(connection_string, wait_ready=True, baud=connection_baudrate)
        print("Connected to Drone")
        return vehicle
    except:
        print("Error connecting Drone")



def message_vision_position_estimate(vehicle, time, x, y, z, roll, pitch, yaw):
    message = vehicle.message_factory.vision_position_estimate_encode(time, x, y, z, roll, pitch, yaw)
    vehicle.send_mavlink(message)
    vehicle.flush()


