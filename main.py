from RealsenseFunctions import *
from ConnectionDroneFunctions import *
import numpy as np
import transformations as tf
from dronekit import *
import time

H_aeroRef_T265Ref = np.array([[0, 0, -1, 0], [1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
H_T265body_aeroBody = np.linalg.inv(H_aeroRef_T265Ref)

pipeline_T265 = init_T265()
pipeline_D435 = init_D435()

vehicle = droneConnection()

try:

    while True:
        frames_T265 = pipeline_T265.wait_for_frames()
        frames_D435 = pipeline_D435.wait_for_frames()

        pose_frame = frames_T265.get_pose_frame()
        depth_frame = frames_D435.get_depth_frame()

        pose_data = pose_frame.get_pose_data()

        H_T265Ref_T265body = tf.quaternion_matrix([pose_data.rotation.w, pose_data.rotation.x, pose_data.rotation.y, pose_data.rotation.z])  # in transformations, Quaternions w+ix+jy+kz are represented as [w, x, y, z]!

        H_T265Ref_T265body[0][3] = pose_data.translation.x
        H_T265Ref_T265body[1][3] = pose_data.translation.y
        H_T265Ref_T265body[2][3] = pose_data.translation.z

        # transform to aeronautic coordinates (body AND reference frame!)
        H_aeroRef_aeroBody = H_aeroRef_T265Ref.dot(H_T265Ref_T265body.dot(H_T265body_aeroBody))

        TaitBryan_rad = np.array(tf.euler_from_matrix(H_aeroRef_aeroBody, 'sxyz'))

        distance_object = get_distance_pixels_inside_region(frames_D435, 1, 0, 0, 640, 480)

        current_time = int(round(time.time() * 1000000))

        message_vision_position_estimate(vehicle, current_time, H_aeroRef_aeroBody[0][3], H_aeroRef_aeroBody[1][3], H_aeroRef_aeroBody[2][3], TaitBryan_rad[0], TaitBryan_rad[1], TaitBryan_rad[2])

        message_distance_sensor(vehicle, current_time, 20, 500, distance_object)


        time.sleep(1.0 / 30)
finally:

    pipeline_T265.stop()
    pipeline_D435.stop()
    vehicle.close()









