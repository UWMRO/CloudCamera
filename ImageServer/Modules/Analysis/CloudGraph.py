import os
import datetime
import typing

import numpy as np
import astropy.io.fits
import matplotlib.pyplot as plt
import matplotlib.gridspec
from scipy import ndimage
from PIL import Image

import CloudParams
from ..Peripherals import StarShotInterface, RainMonitorInterface, TempMonitor, FanInterface


class CloudGraph:
    _img_mask: np.typing.NDArray

    _camera: StarShotInterface.StarShotInterface
    _rain: RainMonitorInterface.RainMonitorInterface
    _temp: TempMonitor.TempMonitor
    _fan: FanInterface.FanInterface

    _rain_10m: bool

    def __init__(self,
                 camera: StarShotInterface.StarShotInterface,
                 rain: RainMonitorInterface.RainMonitorInterface,
                 temp: TempMonitor.TempMonitor,
                 fan: FanInterface.FanInterface,
                 mask: np.ndarray):
        assert (mask.shape[0] == CloudParams.IMG_HxW[0])
        assert (mask.shape[1] == CloudParams.IMG_HxW[1])

        self._camera = camera
        self._rain = rain
        self._temp = temp
        self._fan = fan

        self._rain_10m = False

        if not os.path.exists(CloudParams.RAW_IMAGE_DIR):
            os.mkdir(CloudParams.RAW_IMAGE_DIR)
        if not os.path.exists(CloudParams.ANALYZED_IMAGE_DIR):
            os.mkdir(CloudParams.ANALYZED_IMAGE_DIR)

        self._img_mask = mask

    """
    def dynamic_mask(self, img_dat: np.ndarray, mask: np.ndarray) -> tuple[np.ma.MaskedArray, float, float, float]:
        assert (img_dat.shape[0] == mask.shape[0])
        assert (img_dat.shape[1] == mask.shape[1])

        pre_mask = np.ma.array(img_dat.copy(), mask=mask)

        median = np.ma.median(pre_mask)
        mean = np.ma.mean(pre_mask)
        std_dev = np.ma.std(pre_mask)

        return pre_mask, median, mean, std_dev
    """
    @staticmethod
    def _create_img_dirs(time: datetime.datetime) -> str:
        today_folder: str = time.strftime("%y_%m_%d")
        today_name: str = time.strftime("%H_%M_%S")

        today_raw_path = os.path.join(CloudParams.RAW_IMAGE_DIR, today_folder)
        today_ana_path = os.path.join(CloudParams.ANALYZED_IMAGE_DIR,
                                      today_folder)
        if not os.path.exists(today_raw_path):
            os.mkdir(today_raw_path)
        if not os.path.exists(today_ana_path):
            os.mkdir(today_ana_path)

        return os.path.join(today_folder, today_name)

    def _std_scale_image(self, dat: np.ndarray, med: float, std: float) -> np.ndarray:
        scale: float = 20
        if med < 100:
            scale = 2 * std
        elif med < 200:
            scale = 5 * std

        byte_range: list[float] = [med - scale, med + scale]
        if med < 60:
            byte_range[0] = 1

        return np.clip(dat.copy(), a_min=byte_range[0], a_max=byte_range[1])

    def _finalize_fits(self, img_in: str, img_out: str, exposure: float, gain: float) -> bool:
        return True

    def _create_hist(self,
                     masked_img_dat: np.ndarray,
                     # img_timestamp: datetime.datetime,
                     out_filenamepath: str,
                     exposure: float,
                     gain: float):

        masked_med = np.ma.median(masked_img_dat)
        masked_mean = np.ma.mean(masked_img_dat)
        masked_std = np.ma.std(masked_img_dat)

        plt.clf()
        fig, ax = plt.subplots(2, 2)
        fig.set_size_inches(10, 10)
        fig.tight_layout()
        gs = matplotlib.gridspec.GridSpec(14, 10)

        text_name = out_filenamepath.split("/")[-1]

        ax[0, 0] = plt.subplot(gs[:10, :10])
        ax[0, 0].axis('off')

        # Insert statistical information into the image

        ax[0, 0].text(640, 15, "N", size=20, color="white")
        ax[0, 0].text(640, 1075, "S", size=20, color="white")
        ax[0, 0].text(110, 550, "E", size=20, color="white")
        ax[0, 0].text(1180, 550, "W", size=20, color="white")
        ax[0, 0].text(-30, 980, text_name, size=16,
                      color="white", horizontalalignment='left')
        ax[0, 0].text(-30, 1020, 'Exposure = '+str(exposure)+' [s]',
                      size=16, color="white", horizontalalignment='left', )
        ax[0, 0].text(-30, 1060, 'Gain = '+str(gain),
                      size=16, color="white", horizontalalignment="left")
        ax[0, 0].text(1240, 980, 'Median = %.1f' % (masked_med),
                      size=16, color="white", horizontalalignment='right')
        ax[0, 0].text(1240, 1020, "Mean = %.2f" % (masked_mean),
                      size=16, color="white", horizontalalignment='right')
        ax[0, 0].text(1240, 1060, 'Standard Dev = %.2f' % (
            masked_std), size=16, color="white", horizontalalignment='right')
        ax[0, 0].imshow(masked_img_dat, cmap="gray")

        rain, confidence = self._rain.rain_status()
        print(f"is rain: {rain}, confidence: {confidence}")

        if confidence < 0.75:
            ax[0, 0].text(1000, 50, "Rain = Unknown", size=18, color="yellow")
        elif rain:
            ax[0, 0].text(1000, 50, "Rain = Yes", size=18, color="red")
        else:
            ax[0, 0].text(1000, 50, "Rain = No", size=18, color="green")

        """
        heatStatus = 0
        print('heatStatus: ', heatStatus)
        if heatStatus == 1:
            ax[0, 0].text(1000, 100, "Heat = On", size=18, color="red")
        elif heatStatus == 0:
            ax[0, 0].text(1000, 100, "Heat = Off", size=18, color="blue")
        else:
            ax[0, 0].text(1000, 100, "Heat = Unknown (%s)" %
                          heatStatus, size=18, color="yellow")
        """

        core_temp = self._temp.read_temp_C()
        print('coreTemp [C]: ', core_temp)
        ax[0, 0].text(1000, 150, "Core Temp = %.1f" %
                      core_temp, size=18, color="white")

        """
        num_bins = 30
        bins = np.zeros()
        bin_vals = stats.binned_statistic(masked_img_dat.flatten(), masked_img_dat.flatten(
        ), bins=num_bins, range=(np.ma.min(masked_img_dat), np.ma.max(masked_img_dat)))[0]
        """

        # Plot the histogram
        # = plt.subplot(gs[11:13, :10])
        ax[1, 0] = plt.hist(masked_img_dat.flatten())
        #ax[1, 0].set_xlim(0, 255)
        #ax[1, 0].set_xlabel('Pixel Value', size=16)
        #ax[1, 0].xaxis.label.set_color('white')
        plt.locator_params(axis='y', nbins=6)
        #ax[1, 0].tick_params(axis='x', colors='white', labelsize=12)

        plt.draw()
        fig.savefig(out_filenamepath,)# transparent=True,
                    #facecolor="black", edgecolor='none', clobber=True)
        plt.close()
#        fig.clear()
        # change memory pointer to allow for garbage collection
        fig = None
        gs = None
        ax = None
        # print ('end plot_hist ', (time.time() - self.start))

    async def run_analysis(self, exposure: float, gain: float) -> bool:

        curr_time = datetime.datetime.now()
        img_namepath = CloudGraph._create_img_dirs(curr_time)

        raw_name = os.path.join(CloudParams.RAW_IMAGE_DIR,
                                img_namepath+".fits")
        res = await self._camera.img_from_ssag(raw_name, exposure, gain)
        if not res:
            return False
        img_dat = np.asarray(astropy.io.fits.getdata(raw_name))
        self._finalize_fits(raw_name,
                            os.path.join(
                                CloudParams.ANALYZED_IMAGE_DIR, img_namepath),
                            exposure,
                            gain)

        masked_dat = np.ma.array(img_dat.copy(), mask=self._img_mask)

        masked_med = np.ma.median(masked_dat)
        masked_std = np.ma.std(masked_dat)
        print(f"latest image: {img_namepath.split("/")[-1]}",
              "\npixel statistics:",
              f"\nmedian: {np.ma.median(masked_dat)}, mean: {np.ma.mean(masked_dat)}, std dev: {np.ma.std(masked_dat)}")

        if CloudParams.SCALE_IMG:
            img_dat[self._img_mask] = 0
            img_dat = self._std_scale_image(img_dat, masked_med, masked_std)

        img = ndimage.rotate(img_dat, CloudParams.ROTATION)
        img = ndimage.median_filter(img_dat, 3)
        img_obj = Image.fromarray(img)
        if img_obj.mode != 'RGB':
            img_obj = img_obj.convert('RGB')
        img_obj.save(os.path.join(CloudParams.ANALYZED_IMAGE_DIR,
                     img_namepath), format="PNG")

        self._create_hist(masked_dat,
                          os.path.join(
                              CloudParams.ANALYZED_IMAGE_DIR, img_namepath),
                          exposure,
                          gain)

        return True
