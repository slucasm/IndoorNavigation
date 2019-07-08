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
    connection_string = "COM4"  # Select direction where is the flight controller (we connect with it accross UART ports)
    connection_baudrate = 57600  # Select connection baud rate
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

