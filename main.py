from RealsenseFunctions import *
from ConnectionDroneFunctions import *
import time

pipeline_T265 = init_T265()

vehicle = droneConnection()

print("Connected to Dron")

try:

    frames_T265 = pipeline_T265.wait_for_frames()

    while True:

        pose_frame = frames_T265.get_pose_frame()

        pose_data = pose_frame.get_pose_data()

        data_transformed = transform_data(pose_data)

        H_aeroRef_aeroBody = data_transformed.H_aeroRef_aeroBody

        TaitBryan_rad = data_transformed.TaitBryan_rad

        x = H_aeroRef_aeroBody[0][3]
        y = H_aeroRef_aeroBody[1][3]
        z = H_aeroRef_aeroBody[2][3]

        roll = TaitBryan_rad[0]
        pitch = TaitBryan_rad[1]
        yaw = TaitBryan_rad[2]

        current_time = int(round(time.time() * 1000000))

        message_vision_position_estimate(vehicle, current_time, x, y, x, roll, pitch, yaw)




finally:

    pipeline_T265.stop()
    vehicle.close()









