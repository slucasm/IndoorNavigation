from RealsenseFunctions import *
from ConnectionDroneFunctions import *
import numpy as np
import transformations as tf
from dronekit import *

pipeline_T265 = init_T265()
pipeline_D435 = init_D435()

vehicle = None

while vehicle is None:
    vehicle = droneConnection()

xdata = []
ydata = []
zdata = []

try:
    while True:
        frames_T265 = pipeline_T265.wait_for_frames()
        frames_D435 = pipeline_D435.wait_for_frames()

        pose_frame = frames_T265.get_pose_frame()
        depth_frame = frames_D435.get_depth_frame()

        pose_data = pose_frame.get_pose_data()

        matrix_quaternion = tf.quaternion_matrix([pose_data.rotation.w, -pose_data.rotation.z, pose_data.rotation.x, -pose_data.rotation.y])

        TaitBryan_rad = np.array(tf.euler_from_matrix(matrix_quaternion, 'sxyz'))

        distance_object = get_distance_pixels_inside_region(frames_D435, 1, 0, 0, 640, 480)

        current_time = int(round(time.time() * 1000000))

        x = -pose_data.translation.z
        y = pose_data.translation.x
        z = -pose_data.translation.y

        message_vision_position_estimate(vehicle, current_time, x, y, z, TaitBryan_rad[0], TaitBryan_rad[1], TaitBryan_rad[2])

        message_distance_sensor(vehicle, current_time, 20, 500, distance_object)

        xdata.append(x)
        ydata.append(y)
        zdata.append(z)

        time.sleep(1.0 / 30)

finally:

    pipeline_T265.stop()
    print("LOG: T265 - Save video record as {}_T265.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

    pipeline_D435.stop()
    print("LOG: D435 - Save video record as {}_D435.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

    vehicle.close()
    print("LOG: Connections closed")



    save_to_excel(xdata, ydata, zdata)








