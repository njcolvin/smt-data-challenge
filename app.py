from Game import GameData

years = [1900, 1901, 1902, 1903]
days = [i for i in range(1, 33)]

# for year in years:
#     for day in days:
#         if year == 1900 and day > 9:
#             break
#         if year == 1901 and day > 18:
#             break
#         if year == 1902 and day > 31:
#             break

game = GameData(1903, 31, 'TeamNB', 'TeamA1')
for play_id in game.get_hits()[:, 0]:
    print('play: %d' % play_id)
    game.get_statcast(play_id)
    #game.ball_pos.__generate_baseball_field2D__(play_id)
    game.ball_pos.__generate_baseball_field3D__(play_id)
