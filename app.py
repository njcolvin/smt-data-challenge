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
print(game.get_statcast(9))
game.ball_pos.__generate_baseball_field2D__(9)
game.ball_pos.__generate_baseball_field3D__(9)