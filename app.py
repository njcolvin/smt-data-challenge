from Game import GameData
from os import listdir
import matplotlib.pyplot as plt
import numpy as np

# years = [i for i in range(1900, 1904)]
# days = [i for i in range(1, 33)]

# for year in years:
#     for day in days:
#         if year == 1900 and day > 9:
#             break
#         if year == 1901 and day > 18:
#             break
#         if year == 1902 and day > 31:
#             break

game = GameData(1903, 31, 'TeamNB', 'TeamA1')
#game.infield_batted_balls()
for play_id in np.unique(game.get_hit_events()[:, 0]):
    print('play: %d' % play_id)
    #game.get_statcast(play_id)
    game.plot_play_3d(play_id)
