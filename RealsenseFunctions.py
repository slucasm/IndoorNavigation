import pyrealsense2 as rs
import numpy as np
import datetime
import openpyxl as xlsx


def init_T265():
    pipeline_T265 = rs.pipeline()
    config_T265 = rs.config()
    config_T265.enable_device('905312110153')
    config_T265.enable_stream(rs.stream.pose)
    config_T265.enable_stream(rs.stream.fisheye, 1)
    config_T265.enable_stream(rs.stream.fisheye, 2)
    config_T265.enable_record_to_file("{}_T265.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    pipeline_T265.start(config_T265)
    print("LOG: T265 - Connected with camera")
    print ("LOG: T265 - Start recording")
    return pipeline_T265


def init_D435():
    pipeline_D435 = rs.pipeline()
    config_D435 = rs.config()
    config_D435.enable_device('829212070982')
    config_D435.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config_D435.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 15)
    config_D435.enable_record_to_file("{}_D435.bag".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
    pipeline_D435.start(config_D435)
    print("LOG: D435 - Connected with camera")
    print("LOG: D435 - Start recording")
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


def save_to_excel(xdata,ydata,zdata):
    wb_name = "{}.xlsx".format(datetime.datetime.now().strftime("%Y%m%d"))
    worksheet_name = str(datetime.datetime.now().strftime("%H%M%S"))
    wb = None
    try:
        wb = xlsx.load_workbook(wb_name)
        print("LOG: Created new worksheet in {}" .format(wb_name))
    except:
        print("LOG: Create new .xlsx file")

    if wb is None:
        wb = xlsx.Workbook()

    worksheet = wb.create_sheet(worksheet_name)

    j = 1
    while j <= len(xdata):
        worksheet.cell(row=j, column=1).value = xdata[j-1]
        worksheet.cell(row=j, column=2).value = ydata[j-1]
        worksheet.cell(row=j, column=3).value = zdata[j-1]
        j = j + 1

    wb.save(wb_name)
    print("LOG: Saved trajectory data in {}" .format(wb_name))
