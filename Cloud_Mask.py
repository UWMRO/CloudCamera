import numpy as np


def make_static_mask(self, radius):
    """
    Used to make a static aperture mask, which can be
    multiplied by the analysis image to remove any pixels
    outside the radius from the center.

    Input: Radius to mask from center of image
    Output: Aperture asked numpy array the same size as the image.
    """
    result = []

    for x in range(1024):
        shift_x = x-(1024/2)
        temp_row = []
        for y in range(1280):
            shift_y = y-(1280/2)
            if np.sqrt((shift_x)**2 + (shift_y)**2) > radius:
                temp_row.append(1)
            else:
                temp_row.append(0)
        result.append(temp_row)
    np.save("masks/static_mask", np.asarray(result))

    result = []

    for x in range(1024):
        shift_x = x-(1024/2)
        temp_row = []
        for y in range(1280):
            shift_y = y-(1280/2)
            if np.sqrt((shift_x)**2 + (shift_y)**2) > (radius/2):
                temp_row.append(1)
            else:
                temp_row.append(0)
        result.append(temp_row)
    np.save("masks/small_aperture_mask", np.asarray(result))


    angle_list = [0,1/4.0, 1/2.0, 3/4.0, 1.0, 5/4.0, 3/2.0, 7/4.0]
    print angle_list

    for angle in angle_list:
        theta_low = np.pi * angle - (np.pi/8)
        theta_high = np.pi * angle + (np.pi/8)
        result = []

        for x in range(1024):
            shift_x = x-(1024/2)
            temp_row = []
            for y in range(1280):
                shift_y = y-(1280/2)
                if shift_x == 0:
                    if shift_y >= 0:
                        theta = 0
                    elif shift_y < 0:
                        theta = np.pi
                else:
                    theta = np.arctan(shift_y/shift_x)
                rad = np.sqrt((shift_x)**2 + (shift_y)**2)
                if rad * np.sin(theta) < radius * np.sin(theta_high) or rad * np.sin(theta) < radius * np.sin(theta_low):
                    if rad * np.cos(theta) < radius * np.cos(theta_low) or rad * np.cos(theta) < radius * np.cos(theta_high):
                        temp_row.append(0)
                else :
                    temp_row.append(1)
            result.append(temp_row)
        print "Saving "+str(angle)+" mask"
        np.save("masks/"+str(angle)+"_static_mask", np.asarray(result))


    return "Static mask saved"
