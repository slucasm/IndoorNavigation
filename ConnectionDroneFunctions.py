from pymavlink import mavutil
from dronekit import connect


def droneConnection():
    connection_string = "COM4"
    connection_baudrate = 57600
    print("LOG: Connecting with Drone...")
    vehicle = None

    try:
        vehicle = connect(connection_string, wait_ready=False, baud=connection_baudrate)
        print("LOG: Connected with Drone")
        return vehicle

    except:
        return vehicle


def message_vision_position_estimate(vehicle, time, x, y, z, roll, pitch, yaw):
    message = vehicle.message_factory.vision_position_estimate_encode(time, x, y, z, roll, pitch, yaw)
    vehicle.send_mavlink(message)
    vehicle.flush()


def message_distance_sensor(vehicle, time, min_distance, max_distance, current_distance):

    type = 4 #for uknown distance sensor
    id = 0 #no idea what  means

    message = vehicle.message_factory.distance_sensor_encode(0, min_distance, max_distance, current_distance, type, id, mavutil.mavlink.MAV_SENSOR_ROTATION_NONE, covariance=0)
    vehicle.send_mavlink(message)
    vehicle.flush()

