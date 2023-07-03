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

    def __generate_baseball_field2D__(self):

        names = ['Catcher','Home Plate','1st Base','2nd Base','3rd Base','Pitcher','Outfield','Infield','Coach Box1','Coach Box2','ShortStop','Left Fielder','Center Fielder','Right Fielder']
        coord = [(0.06, 0.08),(0.11, 0.12),(0.43, 0.12),(0.35, 0.43),(0.11, 0.43),(0.265, 0.265),(0.6, 0.6),(0.41, 0.41),(0.07, 0.39),(0.39, 0.07),(0.25, 0.46),(0.3, 0.8),(0.55, 0.55),(0.8, 0.3)]
        color = ['white','gold','gold','gold','gold','white','gold','gold','gold','gold','gold','white','white','white']
        rot = [135,0,0,0,0,135,135,135,90,0,0,150,135,110]
        fontsize=[12,12,12,12,12,12,20,20,10,10,12,12,12,12]

        fig = plt.figure()
        # add a wedge
        fig, ax = plt.subplots(1, figsize=(8,8))
        ax.add_patch(patches.Rectangle((0.0,0.0), 1, 1, facecolor="#247309",  alpha=0.50))

        ax.add_patch(patches.Wedge((0.05,0.05), 0.89, 360, 90, ec="none",edgecolor='orange',facecolor="green", linewidth=2, ))
        ax.add_patch(patches.Wedge((0.1,0.1), 0.52, 360, 90, ec="none",edgecolor='orange',facecolor='white', linewidth=2, ))
        ax.add_patch(patches.Wedge((0.1,0.1), 0.51, 360, 90, ec="none",edgecolor='orange',facecolor='#66431d', linewidth=2, ))
        ax.add_patch(patches.Rectangle((0.1,0.1), 0.32, 0.32, facecolor="white",ec="none"))
        ax.add_patch(patches.Rectangle((0.1,0.1), 0.31, 0.31, facecolor="green",ec="none"))

        ax.add_patch(patches.Circle((0.1,0.1), 0.056, ec="none",facecolor='white',edgecolor='white',linewidth=10))

        ax.add_patch(patches.Circle((0.1,0.1), 0.05, ec="none",facecolor='#66431d',edgecolor='white',linewidth=10))
        ax.add_patch(patches.Wedge((0.1,0.1), 0.056, 360, 90, ec="none",facecolor="#66431d" ))
        ax.add_patch(patches.Rectangle((0.1,0.1), 1.0, 0.01, facecolor="white",ec="none"))
        ax.add_patch(patches.Rectangle((0.1,0.1), 0.01, 1, facecolor="white",ec="none"))
        ax.add_patch(patches.Circle((0.26,0.26), 0.02, ec="none",facecolor='white',edgecolor='white',linewidth=10))

        for i,name in enumerate(names):
            plt.text(coord[i][0],coord[i][1], names[i], color=color[i],rotation=rot[i],fontsize=fontsize[i])

        plt.grid()
        plt.show()

    def __generate_baseball_field3D__(self, play_id:int):
        rows = self.X[self.X[:, 0] == play_id]
        lengths = np.linalg.norm(rows[:, 2:5], axis=1)
        x = rows[:, 2]
        y = rows[:, 3]
        z = rows[:, 4]
        fig_3d = plt.figure(figsize=(8,8))
        ax= fig_3d.add_subplot(projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')

        rect1 = patches.Rectangle((0.0,0.0), 1, 1, facecolor="#247309",  alpha=0.1)
        ax.add_patch(rect1)
        art3d.pathpatch_2d_to_3d(rect1, z=0, zdir="z",)

        wedge1 = patches.Wedge((0.05,0.05), 0.89, 360, 90,alpha=0.1,facecolor="green", linewidth=2, )
        ax.add_patch(wedge1)
        art3d.pathpatch_2d_to_3d(wedge1, z=0, zdir="z")

        wedge2 = patches.Wedge((0.1,0.1), 0.52, 360, 90, alpha=0.2,facecolor='#66431d', linewidth=2, )
        ax.add_patch(wedge2)
        art3d.pathpatch_2d_to_3d(wedge2, z=0, zdir="z")

        rect2 = patches.Rectangle((0.1,0.1), 0.32, 0.32,alpha=0.1, facecolor="white")
        ax.add_patch(rect2)
        art3d.pathpatch_2d_to_3d(rect2, z=0, zdir="z")

        rect3 = patches.Rectangle((0.1,0.1), 0.31, 0.31, alpha=0.2, facecolor="green")
        ax.add_patch(rect3)
        art3d.pathpatch_2d_to_3d(rect3, z=0, zdir="z")

        circle1 = patches.Circle((0.1,0.1), 0.056,alpha=0.1,facecolor='white')
        ax.add_patch(circle1)
        art3d.pathpatch_2d_to_3d(circle1, z=0, zdir="z")

        circle2 = patches.Circle((0.1,0.1), 0.05,alpha=0.1,facecolor='#66431d')
        ax.add_patch(circle2)
        art3d.pathpatch_2d_to_3d(circle2, z=0, zdir="z")

        wedge4 = patches.Wedge((0.1,0.1), 0.056, 360, 90,alpha=1,facecolor="#66431d" )
        ax.add_patch(wedge4)
        art3d.pathpatch_2d_to_3d(wedge4, z=0, zdir="z")

        rect4 = patches.Rectangle((0.1,0.1), 0.89, 0.01, facecolor="white",alpha=1)
        ax.add_patch(rect4)
        art3d.pathpatch_2d_to_3d(rect4, z=0, zdir="z")


        rect5 = patches.Rectangle((0.1,0.1), 0.01, 0.89, facecolor="white",alpha=1)
        ax.add_patch(rect5)
        art3d.pathpatch_2d_to_3d(rect5, z=0, zdir="z")

        circle3 = patches.Circle((0.26,0.26), 0.02, facecolor='white',alpha=1)
        ax.add_patch(circle3)
        art3d.pathpatch_2d_to_3d(circle3, z=0, zdir="z")
        
        names = ['Catcher','HP','Pitcher','CF']
        coord = [(0.06, 0.08),(0.11, 0.12),(0.265, 0.265),(0.65, 0.65)]
        color = ['blue','brown','blue','brown']
        rot = [135,0,135,9,45,0,135]
        fontsize=[12,12,12,10,12,12,]
        
        for J,name in enumerate(names):
            ax.text(coord[J][0],coord[J][1], 0, names[J], color=color[J],rotation=rot[J],
                    fontsize=fontsize[J],zdir="z",verticalalignment='center')

        ax.text(0.4,0.004,0,"Coach Box",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.004,0.4,0,"Coach Box",color='Brown',fontsize=12,zdir=(0,1,0),verticalalignment='center')
        ax.text(0.12,0.43,0,"B3",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.35, 0.43,0,"B2",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.43, 0.12,0,"B1",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.25, 0.46,0,"SS",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.8, 0.3,0,"RF",color='Brown',fontsize=12,zdir=(0,1,0),verticalalignment='center')
        ax.text(0.3, 0.8,0,"LF",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.95,"LF : Left Fielder",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.9,"CF : Central Fielder",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.85,"RF : Right Fielder",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.8,"SS : ShortStaff",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.75,"B1 : First Baseman",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.70,"B2 : Second Baseman",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')
        ax.text(0.2, 1,0.65,"B3 : Third Baseman",color='Brown',fontsize=12,zdir=(1,0,0),verticalalignment='center')

        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.set_xlim3d(0, 1)
        ax.set_ylim3d(0, 1)
        ax.set_zlim3d(0, 1)

        #plt.show()