from pymavlink import *
from dronekit import *




def droneConnection():
    connection_string = '/dev/serial0'
    connection_baudrate = 921600

    try:
        vehicle = connect(connection_string, wait_ready = True, baud = connection_baudrate)
    except:
        print("Error connecting Drone")

    if vehicle:
        return vehicle
    else:
        return False


