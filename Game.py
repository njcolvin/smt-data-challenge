from numpy import genfromtxt
from os import listdir
from Ball import BallPosition
from Player import PlayerPosition

class GameData():

    def __init__(self, year:int=1900, day:int=1) -> None:
        self.year = year
        self.day = day

        # get filename
        ball_pos_prefix = 'ball_pos-%d_%02d' % (year, day)        
        for f in listdir('./data/ball_pos/'):
            if f.startswith(ball_pos_prefix):
                self.game_str = f.lstrip('ball_pos-')
                break

        # get teams from filename
        self.away_team = self.game_str.split('_')[2]
        self.home_team = self.game_str.split('_')[3].rstrip('.csv')

        table_suffix = '-%d_%02d_%s_%s.csv' % (self.year, self.day, self.away_team, self.home_team)
        
        # get tables
        self.ball_pos = BallPosition(table_suffix)
        self.game_events = GameEvents(table_suffix)
        self.game_info = GameInfo(table_suffix)
        
        year_dir = '-%d_%s' % (year, self.home_team)
        dir_path = './data/player_pos/' + self.home_team + '/player_pos' + year_dir
        file_path = dir_path + '/player_pos' + table_suffix
        self.player_pos = PlayerPosition(file_path)

    def __str__(self) -> str:
        return self.game_str
    
    def get_away_roster(self) -> list:
        team_info = genfromtxt('./data/team_info.csv', skip_header=1, delimiter=',', dtype=None, encoding=None)
        return [x[1] for x in team_info if x[2] == self.year and x[0].strip('"').strip("'") == self.away_team]
    
    def get_home_roster(self) -> list:
        team_info = genfromtxt('./data/team_info.csv', skip_header=1, delimiter=',', dtype=None, encoding=None)
        return [x[1] for x in team_info if x[2] == self.year and x[0].strip('"').strip("'") == self.home_team]

class GameEvents:

    def __init__(self, suffix:str) -> None:
        self.X = genfromtxt('./data/game_events/game_events' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)

class GameInfo:

    def __init__(self, suffix:str) -> None:
        self.X = genfromtxt('./data/game_info/game_info' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)