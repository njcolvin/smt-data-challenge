from matplotlib.axes import Axes
from numpy import genfromtxt

class BallPosition:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = genfromtxt('./data/ball_pos/ball_pos' + table_suffix, skip_header=1, delimiter=',', dtype=float, encoding=None,
                            usecols=range(2, 7))

    def __plot2d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        ax.scatter(x, y, c='r', marker='o')

    def __plot3d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        z = rows[:, 4]
        ax.scatter(x, y, z, c='r', marker='o')