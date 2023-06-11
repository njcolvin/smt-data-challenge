from numpy import genfromtxt
from os import path, listdir

class GameData():
    def __init__(self, year:int=1900, day:int=1) -> None:
        ball_pos_prefix = 'ball_pos-%d_%02d' % (year, day)
        game_str = next(f for f in listdir('./data/ball_pos/') if f.startswith(ball_pos_prefix))
        
        self.away_team = game_str.split('_')[3].lstrip('Team')
        self.home_team = game_str.split('_')[4].lstrip('Team').rstrip('.csv')

        suffix = '-%d_%02d_Team%s_Team%s.csv' % (year, day, self.away_team, self.home_team)
        
        self.ball_pos = genfromtxt('./data/ball_pos/ball_pos' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)
        self.game_events = genfromtxt('./data/game_events/game_events' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)
        self.game_info = genfromtxt('./data/game_info/game_info' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)
        
        team_dir = 'Team%s' % self.home_team
        year_dir = '-%d_Team%s' % (year, self.home_team)
        dir_path = './data/player_pos/' + team_dir + '/player_pos' + year_dir
        file_path = dir_path + '/player_pos' + suffix
        
        if path.exists(dir_path) and path.isfile(file_path):
            self.player_pos = genfromtxt(file_path, skip_header=1, delimiter=',', dtype=None, encoding=None)
        else:
            self.player_pos = None
