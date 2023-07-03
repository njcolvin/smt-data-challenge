from numpy import genfromtxt
import matplotlib.pyplot as plt
from matplotlib import style
from sportypy.surfaces import baseball
import matplotlib.patches as patches
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np

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
            milb.scatter(x, y, color = 'r')
        
        plt.show()

    def __generate_baseball_field2D__(self, play_id:int):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot()

        ax.add_patch(patches.Rectangle((-400,-26), 800, 426, facecolor="#247309",  alpha=0.50))
        ax.add_patch(patches.Wedge((0,-26), 400, 45, 135, ec="none",edgecolor='orange',facecolor="green", linewidth=2, ))
        ax.add_patch(patches.Wedge((0,0), 208, 45, 135, ec="none",edgecolor='orange',facecolor='white', linewidth=2, ))
        ax.add_patch(patches.Wedge((0,0), 204, 45, 135, ec="none",edgecolor='orange',facecolor='#66431d', linewidth=2, ))
        ax.add_patch(patches.Rectangle((0,0), 128, 128, angle=45, facecolor="white",ec="none"))
        ax.add_patch(patches.Rectangle((0,0), 124, 124, angle=45, facecolor="green",ec="none"))
        ax.add_patch(patches.Circle((0,0), 22.4, ec="none",facecolor='white',edgecolor='white',linewidth=10))
        ax.add_patch(patches.Circle((0,0), 20, ec="none",facecolor='#66431d',edgecolor='white',linewidth=10))
        ax.add_patch(patches.Wedge((0,0), 22.4, 45, 135, ec="none",facecolor="#66431d" ))
        ax.add_patch(patches.Rectangle((0,0), 400, 4, angle=45, facecolor="white",ec="none"))
        ax.add_patch(patches.Rectangle((0,0), 4, 400, angle=45, facecolor="white",ec="none"))
        ax.add_patch(patches.Circle((0,60), 9, ec="none",facecolor='white',edgecolor='white',linewidth=10))

        ax.scatter(x, y, c='r', marker='o')

        plt.show()

    def __generate_baseball_field3D__(self, play_id:int):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        z = rows[:, 4]
        fig_3d = plt.figure(figsize=(8,8))
        ax= fig_3d.add_subplot(projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')

        # ground 
        rect1 = patches.Rectangle((-400,-26), 800, 426, facecolor="#247309",  alpha=0.1)
        ax.add_patch(rect1)
        art3d.pathpatch_2d_to_3d(rect1, z=0, zdir="z",)

        # outfield
        wedge1 = patches.Wedge((0,-26), 400, 45, 135,alpha=0.1,facecolor="green", linewidth=2, )
        ax.add_patch(wedge1)
        art3d.pathpatch_2d_to_3d(wedge1, z=0, zdir="z")

        # infield
        wedge2 = patches.Wedge((0,0), 208, 45, 135, alpha=0.2,facecolor='#66431d', linewidth=2, )
        ax.add_patch(wedge2)
        art3d.pathpatch_2d_to_3d(wedge2, z=0, zdir="z")

        rect3 = patches.Rectangle((0,0), 124, 124, angle=45, alpha=0.2, facecolor="green")
        ax.add_patch(rect3)
        art3d.pathpatch_2d_to_3d(rect3, z=0, zdir="z")

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_xlim3d(-400, 400)
        ax.set_ylim3d(-26, 400)
        ax.set_zlim3d(0, 140)

        plt.show()