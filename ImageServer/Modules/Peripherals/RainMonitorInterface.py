
class RainMonitorInterface:
    def __init__(self):
        pass

    def rain_status(self) -> tuple[bool, float]:
        return False, 1
