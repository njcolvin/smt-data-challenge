from numpy import genfromtxt

class Player:

    def __init__(self, id:int) -> None:
        self.id = id
        # each stat is an average
        self.base_run_time = float
        self.bat_handedness = int # 0 = right, 1 = left
        self.arm_handedness = int
        self.exit_velo = float
        self.launch_angle = float
        self.launch_speed = float
        self.groundball_pull_pct = float
        self.flyball_pull_pct = float
        self.range = float
        self.transfer_time = float
        self.arm_strength = float


class PlayerPosition:

    def __init__(self, filename:str) -> None:
        self.X = genfromtxt(filename, skip_header=1, delimiter=',', dtype=None, encoding=None)

class Alignment:

    def __init__(self) -> None:
        pass