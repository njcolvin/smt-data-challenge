from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib import style
from sportypy.surfaces import baseball

class BallPosition:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = genfromtxt('./data/ball_pos/ball_pos' + table_suffix, skip_header=1, delimiter=',', dtype=float, encoding=None,
                            usecols=range(2, 7))
        
    def plot_play(self, play_id:int, in_3d:bool):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        z = rows[:, 4]

        if in_3d:
            style.use('ggplot')
            fig = plt.figure()
            ax1 = fig.add_subplot(111, projection='3d')


            ax1.scatter(x, y, z, c='r', marker='o')
            ax1.set_xlabel('x axis')
            ax1.set_ylabel('y axis')
            ax1.set_zlabel('z axis')
        else:
            milb = baseball.MiLBField()
            fig, ax = plt.subplots(1, 1)
            milb.draw(ax=ax)
            milb.scatter(x, y, color = "#fec52e")
        
        plt.show()