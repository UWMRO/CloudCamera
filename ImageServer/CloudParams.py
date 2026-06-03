'''
Parameter file for CloudCam options.
'''

import typing
import os


# misc
CAM_NAME: typing.Final[str] = "Star Shot Auto Guider"

# directories
repo_dir = os.getcwd()
if repo_dir.split("/")[-1] == "ImageServer":
    repo_dir = repo_dir.removesuffix("ImageServer")
TOP_LEVEL_REPO_DIR: typing.Final[str] = repo_dir

CAMERA_INTERFACE_PROGRAM: typing.Final[str] = os.path.join(
    TOP_LEVEL_REPO_DIR, "ImageTaker/build/ImageTaker_exe")
BINARY_IMG_DIR: typing.Final[str] = os.path.join(
    TOP_LEVEL_REPO_DIR, "tmp_img", )
BINARY_IMG_LABEL: typing.Final[str] = os.path.join(
    BINARY_IMG_DIR, "curr_img.bin")
RAW_IMAGE_DIR: typing.Final[str] = os.path.join(TOP_LEVEL_REPO_DIR, "raw")
ANALYZED_IMAGE_DIR: typing.Final[str] = os.path.join(
    TOP_LEVEL_REPO_DIR, "analyzed")

WEBSITE_DIR: typing.Final[str] = os.path.join(
    TOP_LEVEL_REPO_DIR, "ImageServerSite")


# image:
IMG_HxW: typing.Final[tuple[int, int]] = (1024, 1280)

# exposure
MIN_MEDIAN: typing.Final[float] = 40  # Lower limit for median value
MAX_MEDIAN: typing.Final[float] = 100  # Upper limit for median value
STEP_SIZE: typing.Final[float] = 0.60  # Exposure scaling step size, %
EXPOSE: typing.Final[float] = 1  # Set starting exposure
MAX_EXPOSE: typing.Final[float] = 10
GAIN: typing.Final[float] = 1  # Set starting gain
MAX_GAIN: typing.Final[float] = 5

# scaling
SCALE_IMG: typing.Final[bool] = True  # Toggle image scaling
BINARY_EROSION: typing.Final[bool] = False  # Toggle binary erosion filtering
ROTATION: typing.Final[int] = -12  # How much to rotate the image

# masking
RADIUS: typing.Final[int] = 500  # large aperture mask radius, pixels
X_CENTER: typing.Final[int] = int(1024/2)  # Center pixel on x axis 512
Y_CENTER: typing.Final[int] = int(1340/2)  # Center pixel on y axis 670

# subroutines
IMAGE_TAKING_RATE_HZ: typing.Final[float] = 1/60
WEBSITE_UPDATE_RATE_HZ: typing.Final[float] = 5

# peripherals
TEMP_MONITOR_PATH: typing.Final[str] = "/sys/class/thermal/thermal_zone0/temp"
FAN_PINS: typing.Final[tuple[int, ...]] = ()
