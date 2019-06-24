import pyrealsense2 as rs
import numpy as np
import transformations as tf

H_aeroRef_T265Ref = np.array([[0, 0, -1, 0], [1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
H_T265body_aeroBody = np.linalg.inv(H_aeroRef_T265Ref)

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

class dataTransformed:
    def __init__(self, H_aeroRef_aeroBody, TaitBryan_rad):
        self.H_aeroRef_aeroBody = H_aeroRef_aeroBody
        self.TaitBryan_rad = TaitBryan_rad

def transform_data(pose_data):
    H_T265Ref_T265body = tf.quaternion_matrix([pose_data.rotation.w, pose_data.rotation.x, pose_data.rotation.y, pose_data.rotation.z])  # in transformations, Quaternions w+ix+jy+kz are represented as [w, x, y, z]!

    H_T265Ref_T265body[0][3] = pose_data.translation.x
    H_T265Ref_T265body[1][3] = pose_data.translation.y
    H_T265Ref_T265body[2][3] = pose_data.translation.z

    # transform to aeronautic coordinates (body AND reference frame!)
    H_aeroRef_aeroBody = H_aeroRef_T265Ref.dot(H_T265Ref_T265body.dot(H_T265body_aeroBody))

    TaitBryan_rad = np.array(tf.euler_from_matrix(H_aeroRef_aeroBody, 'sxyz'))

    return dataTransformed(H_aeroRef_aeroBody, TaitBryan_rad)