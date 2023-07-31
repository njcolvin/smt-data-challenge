import numpy as np
from matplotlib.axes import Axes

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
        self.X = np.genfromtxt(filename, skip_header=1, delimiter=',', dtype=float, encoding=None,
                               usecols=range(2, 7))

    def positions(self):
        return np.unique(self.X[:, 2])

    def __plot2d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        for pos in range(1, 20):
            pos_rows = rows[rows[:, 2] == pos]
            x = pos_rows[:, 3]
            y = pos_rows[:, 4]
            ax.scatter(x, y, c='b', marker='o')

    def __plot3d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        for pos in range(1, 20):
            pos_rows = rows[rows[:, 2] == pos]
            x = pos_rows[:, 3]
            y = pos_rows[:, 4]
            z = np.zeros(np.shape(x))
            ax.scatter(x, y, z, c='b', marker='o')