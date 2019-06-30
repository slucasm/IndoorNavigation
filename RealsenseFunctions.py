import pyrealsense2 as rs
import numpy as np

def init_T265():
    pipeline_T265 = rs.pipeline()
    config_T265 = rs.config()
    config_T265.enable_device('905312110153')
    config_T265.enable_stream(rs.stream.pose)
    pipeline_T265.start(config_T265)
    return pipeline_T265

def init_D435():
    pipeline_D435 = rs.pipeline()
    config_D435 = rs.config()
    config_D435.enable_device('829212070982')
    config_D435.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    pipeline_D435.start(config_D435)
    return pipeline_D435

def get_distance_pixels_inside_region(frames_D435, minimum_distance, x_up, y_up, x_down, y_down):
    depth_frames = frames_D435.get_depth_frame()
    list_distances = []
    j = y_up
    while (j < y_down):
        i = x_up
        while (i < x_down):
            pixel_distance = depth_frames.get_distance(i, j)
            if (pixel_distance < minimum_distance and pixel_distance != 0):
                list_distances.append(pixel_distance)
            i = i + 1
        j = j + 1

    hist, bins = np.histogram(list_distances, bins='auto')

    index = np.argmax(hist)

    if len(list_distances) > 4000:
        return bins[index]*100
    else:
        return 1000

    mean_distance = bins[index]

    return mean_distance