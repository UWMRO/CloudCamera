import asyncio
import os
import time

import CloudParams
from Modules.Peripherals import StarShotInterface, RainMonitorInterface, TempMonitor, FanInterface
from Modules.Analysis import mask_creator, CloudGraph
from Modules.Server import ImgServer


async def update_images():
    print("starting peripherals")
    cam = StarShotInterface.StarShotInterface()
    rain_sensor = RainMonitorInterface.RainMonitorInterface()
    temp_sensor = TempMonitor.TempMonitor(CloudParams.TEMP_MONITOR_PATH)
    fan_sensor = FanInterface.FanInterface()

    print("testing peripherals")
    cam_test = await cam.test_program()
    assert (cam_test == True)

    print("staring data analysis")
    analysis = CloudGraph.CloudGraph(cam,
                                     rain_sensor,
                                     temp_sensor,
                                     fan_sensor,
                                     mask_creator.create_circle_mask(CloudParams.RADIUS,
                                                                     CloudParams.IMG_HxW,
                                                                     CloudParams.X_CENTER,
                                                                     CloudParams.Y_CENTER))

    while True:
        start_t = time.time()

        res = await analysis.run_analysis(1, 1)
        print("image succeeded?:", res)

        current_t = time.time()
        await asyncio.sleep((current_t-start_t) + 1.0/CloudParams.IMAGE_TAKING_RATE_HZ)


async def update_server():
    print("img")

    app = ImgServer.ImgServer()

    @app.route('/home')
    async def home():
        return str(open(os.path.join(CloudParams.WEBSITE_DIR, "home.html"), "r").read())

    @app.route('/images')
    async def images():
        return str(open(os.path.join(CloudParams.WEBSITE_DIR, "images.html"), "r").read())

    @app.route('/statistics')
    async def statistics():
        return str(open(os.path.join(CloudParams.WEBSITE_DIR, "statistics.html"), "r").read())

    @app.route('/contact')
    async def contact():
        return str(open(os.path.join(CloudParams.WEBSITE_DIR, "contact.html"), "r").read())

    await app.serve(8000)


async def main():
    await asyncio.gather(update_server(), update_images())

    while True:
        pass

if __name__ == "__main__":
    asyncio.run(main())
