""""

INDOOR NAVIGATION LOW COST SYSTEM FOR DRONES

Developed by: Sergi Lucas Millan
Email: sergilucasmillan@hotmail.com
Tutor: Oscar Casas Piedrafita
Center: UPC - EETAC

File description: includes functions where drone flight controller (Pixhawk 2.4.8) is involved

"""

from pymavlink import mavutil
from dronekit import connect

# Establish connection with flight controller
def droneConnection():
    connection_string = '/dev/serial0'  # Select direction where is the flight controller (we connect with it accross UART ports)
    connection_baudrate = 921600  # Select connection baud rate
    print("LOG: Connecting with Drone...")
    vehicle = None

    try:
        vehicle = connect(connection_string, wait_ready=False, baud=connection_baudrate)
        print("LOG: Connected with Drone")
        return vehicle

    except:
        return vehicle

# Send messages with position and orientation to flight controller
def message_vision_position_estimate(vehicle, time, x, y, z, roll, pitch, yaw):
    message = vehicle.message_factory.vision_position_estimate_encode(time, x, y, z, roll, pitch, yaw)
    vehicle.send_mavlink(message)
    vehicle.flush()

# Send messages with distance to object
def message_distance_sensor(vehicle, time, min_distance, max_distance, current_distance):

    type = 4  # For uknown distance sensor
    id = 0  # No idea what  means

    message = vehicle.message_factory.distance_sensor_encode(0, min_distance, max_distance, current_distance, type, id, mavutil.mavlink.MAV_SENSOR_ROTATION_NONE, covariance=0)
    vehicle.send_mavlink(message)
    vehicle.flush()

def message_set_home_position(vehicle):

    lat = 412751720
    lon = 19845350

    message = vehicle.message_factory.set_home_position_encode(int(vehicle._master.source_system),lat,lon, 0, 0, 0, 0, [1, 0, 0, 0], 0, 0, 1)
    vehicle.send_mavlink(message)
    vehicle.flush()

def message_set_gps_global_origin_position(vehicle):

    lat = 412751720
    lon = 19845350

    message = vehicle.message_factory.set_gps_global_position_origin_encode(int(vehicle._master.source_system), lat, lon, 0)
    vehicle.send_mavlink(message)
    vehicle.flush()