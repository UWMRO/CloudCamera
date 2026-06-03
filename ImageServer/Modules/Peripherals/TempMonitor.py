

class TempMonitor:
    _temp_path: str

    def __init__(self, temp_path: str):
        self._temp_path = temp_path

    def read_temp_C(self) -> float:
        return float(open(self._temp_path).read()) / 1e3

    def read_temp_F(self, ) -> float:
        return (self.read_temp_C() * 9/5) + 32
