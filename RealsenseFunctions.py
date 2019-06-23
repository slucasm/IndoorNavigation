import pyrealsense2 as rs
import numpy as np

def init_T265():
    pipeline_T265 = rs.pipeline()
    config_T265 = rs.config()
    config_T265.enable_device('905312110153')
    config_T265.enable_stream(rs.stream.pose, 848, 800, rs.format.six_dof, 200)
    pipeline_T265.start(config_T265)
    return pipeline_T265

def init_D435():
    pipeline_D435 = rs.pipeline()
    config_D435 = rs.config()
    config_D435.enable_device('829212070982')
    config_D435.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    pipeline_D435.start(config_D435)
    return pipeline_D435