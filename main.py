""""

INDOOR NAVIGATION LOW COST SYSTEM FOR DRONES

Developed by: Sergi Lucas Millan
Email: sergilucasmillan@hotmail.com
Tutor: Oscar Casas Piedrafita
Center: UPC - EETAC

File description: main code

"""

from RealsenseFunctions import *
from ConnectionDroneFunctions import *
import numpy as np
import transformations as tf
from dronekit import *

# Configure cameras and establish connections
pipeline_T265 = init_T265()
#pipeline_D435 = init_D435()

vehicle = None

while vehicle is None:
    # Start connection with flight controller
    vehicle = droneConnection()

message_set_gps_global_origin_position(vehicle)
message_set_home_position(vehicle)

xdata = []
ydata = []
zdata = []

try:
    while True:
	
#	print("Battery: %s" % vehicle.battery)

        # Start receiving images from both cameras
        frames_T265 = pipeline_T265.wait_for_frames()
#        frames_D435 = pipeline_D435.wait_for_frames()

        # Get frames from cameras (trajectory and depth frames)
        pose_frame = frames_T265.get_pose_frame()
#        depth_frame = frames_D435.get_depth_frame()

        # Get trajectory data from frame
        pose_data = pose_frame.get_pose_data()

        # Create quaternion matrix about vector rotation [wxyz] from trajectory data (with correct reference frame)
        matrix_quaternion = tf.quaternion_matrix([pose_data.rotation.w, -pose_data.rotation.z, pose_data.rotation.x, -pose_data.rotation.y])

        # Get TaitBryan angles in rad from quaternion matrix
        TaitBryan_rad = np.array(tf.euler_from_matrix(matrix_quaternion, 'sxyz'))

        # Execute function to calculate distance to object
#        distance_object = get_distance_pixels_inside_region(frames_D435, 1, 0, 0, 640, 480)

        # Get UNIX time
        current_time = int(round(time.time() * 1000000))

        # Rotation to correct reference frame
        x = -pose_data.translation.z
        y = pose_data.translation.x
        z = pose_data.translation.y

        # Send message to flight controller about position and rotation
        message_vision_position_estimate(vehicle, current_time, x, y, z, TaitBryan_rad[0], TaitBryan_rad[1], TaitBryan_rad[2])

        # Send message to flight controller of distance to object
#        message_distance_sensor(vehicle, current_time, 20, 500, distance_object)

        # Save trajectory data in arrays
        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

        time.sleep(1.0 / 30)

finally:

    # Close connections
    pipeline_T265.stop()
   #print("LOG: T265 - Save video record as {}_T265.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

#    pipeline_D435.stop()
   # print("LOG: D435 - Save video record as {}_D435.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

    vehicle.close()
    print("LOG: Connections closed")

    # Save trajectory data to excel file
    save_to_excel(xdata, ydata, zdata)








