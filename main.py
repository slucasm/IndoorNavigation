from RealsenseFunctions import *
from ConnectionDroneFunctions import *

pipeline_T265 = init_T265()

vehicle = None

while None != vehicle:
    vehicle = droneConnection()

print("Connected to Dron")

try:
    frames_T265 = pipeline_T265.wait_for_frames()

    pose_frame = frames_T265.get_pose_frame()

    pose_data = pose_frame.get_pose_data()

finally:
    pipeline_T265.stop()
    vehicle.stop()









