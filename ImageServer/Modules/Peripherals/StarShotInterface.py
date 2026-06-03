
import typing
import asyncio
import os
import time

import astropy.io.fits as fits
import numpy as np

import CloudParams


class StarShotInterface:
    _SSAG_TEST_CMD: typing.Final[str] = "test"
    _SSAG_IMG_CMD: typing.Final[str] = "image"

    def __init__(self):
        if not os.path.exists(CloudParams.BINARY_IMG_DIR):
            os.mkdir(CloudParams.BINARY_IMG_DIR)

    def _form_ssag_test_cmd(self) -> tuple[str, str, str, str]:
        return (self._SSAG_TEST_CMD, "aa", "bb", "cc")

    def _form_ssag_cmd(self, file_namepath: str, exposure_time: float, gain: float) -> tuple[str, str, str, str]:
        return (self._SSAG_IMG_CMD, file_namepath, str(exposure_time), str(gain))

    async def _run_ssag_script(self, args: tuple[str, ...]) -> tuple[int, bytes, bytes]:
        full_args = ["sudo", CloudParams.CAMERA_INTERFACE_PROGRAM]
        full_args.extend(args)
        ssag_script = await asyncio.create_subprocess_exec(
            *full_args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await ssag_script.communicate()
        if ssag_script.returncode != None:
            return (ssag_script.returncode, stdout, stderr)
        return (0, stdout, stderr)

    async def test_program(self) -> bool:
        try:
            results = await self._run_ssag_script(self._form_ssag_test_cmd())
            if (results[0] == 0) and (b"acknowledge test" in results[1]):
                return True
            else:
                print(CloudParams.CAM_NAME,
                      "interface script is not responding as expected to test")
        except FileNotFoundError:
            print("cannot find", CloudParams.CAM_NAME, "interface script at the expected location:",
                  CloudParams.CAMERA_INTERFACE_PROGRAM)
        print("please ensure that the script is properly installed\n(have you followed README.md and successfully run setup.sh?)")
        return False

    async def _expose(self, raw_namepath: str, exposure: float, gain: float) -> bool:
        script_arg = self._form_ssag_cmd(
            raw_namepath, exposure, gain)
        results = await self._run_ssag_script(script_arg)

        if results[0] != 0:
            print(f"taking image failed with argument: {script_arg}")
            if results[1]:
                print("stdout:", str(results[1]))
            if results[2]:
                print("stderr:", str(results[2]))
            return False
        return True

    @staticmethod
    def _create_header(exp: float, gain: float) -> fits.Header:
        pri_header = fits.Header()
        pri_header['COMMENT'] = 'MRO Guider Camera'
        pri_header['COMMENT'] = 'Orion Star Shoot Auto Guider'
        pri_header['IMAGTYP'] = "guide"
        pri_header['EXPTIME'] = str(exp)
        pri_header['CCDBIN1'] = 1
        pri_header['CCDBIN2'] = 1
        pri_header['GAIN'] = gain
        pri_header['RN'] = None
        return pri_header

    async def img_from_ssag(self, file_namepath: str, exposure: float, gain: float) -> bool:

        if not await self._expose(CloudParams.BINARY_IMG_LABEL, exposure, gain):
            return False

        bin_data = np.fromfile(os.path.join(CloudParams.BINARY_IMG_DIR, CloudParams.BINARY_IMG_LABEL), dtype="u1").reshape(
            CloudParams.IMG_HxW)

        header = self._create_header(exposure, gain)
        hdu_list = fits.HDUList([fits.PrimaryHDU(bin_data, header=header)])

        if ".fits" not in file_namepath:
            file_namepath +=".fits"
        hdu_list.writeto(file_namepath)

        return True
