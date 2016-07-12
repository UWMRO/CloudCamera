#! /usr/bin/python

"""
Cloud_Mask.py
Used to produce mask files for the CloudCam.

Can be used to make a large aperture mask,
small aperture mask, and directional wedge
masks.
"""

import numpy as np


class CloudMask(object):
    def __init__(self):
        self.radius = 500
        self.xcenter = 562
        self.ycenter = 590


    def make_aperture_mask(self, radius):
        """
        Used to make a static aperture mask, which can be
        multiplied by the analysis image to remove any pixels
        outside the radius from the center.

        Input: Radius to mask from center of image

        Output: Aperture masked numpy array the same size as the image.
                Saved as a numpy mask file
        """
        result = []

        print "Producing aperture mask with radius = "+str(radius)
        for x in range(1024):
            shift_x = x-(self.xcenter)
            temp_row = []
            for y in range(1280):
                shift_y = y-(self.ycenter)
                if np.sqrt((shift_x)**2 + (shift_y)**2) > radius:
                    temp_row.append(1)
                else:
                    temp_row.append(0)
            result.append(temp_row)
        np.save("masks/aperture_mask_"+str(radius), np.asarray(result))
        return "Aperture mask saved"


    def make_wedge_mask(self, radius):
        """
        Used to produce directional wedge shaped masks

        Input:
            radius (float)      How large should the wedges extend from center

        Output:
            Saved wedge shaped mask files in masks/
        """

        angle_list = [-3/4.0, -1/2.0, -1/4.0, 0.0, 1/4.0, 1/2.0, 3/4.0, 1.0]
        #angle_list = [1.0]

        for angle in angle_list:
            theta_low = (np.pi * angle) - (np.pi / 8)
            theta_high = (np.pi * angle) + (np.pi / 8)
            if theta_high > np.pi:
                theta_high = theta_high - (2 * np.pi)

            print "Theta low = "+str(theta_low / np.pi)
            print "Theta high = "+str(theta_high / np.pi)

            result = []
            # Move coordinate system to center of image
            for x in range(1024):
                shift_x = x-(self.xcenter)
                temp_row = []
                for y in range(1280):
                    shift_y = y-(self.ycenter)

                    theta = np.arctan2(shift_y,shift_x)
                    rad = np.sqrt((shift_x)**2 + (shift_y)**2)

                    if angle == 1.0:
                        #Only look at points inside the radius
                        if rad < radius:
                            if theta_low < theta:
                                temp_row.append(0)
                            elif theta_high > theta:
                                temp_row.append(0)
                            else:
                                temp_row.append(1)
                        else :
                            temp_row.append(1)

                    else:
                        #Only look at points inside the radius
                        if rad < radius:
                            if theta_low < theta and theta < theta_high:
                                temp_row.append(0)
                            else:
                                temp_row.append(1)
                        else :
                            temp_row.append(1)
                result.append(temp_row)

            for i in result[self.xcenter-10:self.xcenter+10]:
                print i[self.ycenter-10:self.ycenter+10]

            print "Saving "+str(int(angle * 4) + 4)+" mask"
            np.save("masks/"+str(int(angle * 4) + 4)+"_wedge_mask", np.asarray(result))


        return "Wedge masks saved"

if __name__ == "__main__":
    cm = CloudMask()
    #cm.make_aperture_mask(500)
    #cm.make_aperture_mask(300)
    cm.make_wedge_mask(300)
