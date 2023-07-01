import numpy as np
from numpy import genfromtxt
from Ball import BallPosition
from Player import PlayerPosition
from Statcast import Statcast
from Glossary import teams

class GameData():

    def __init__(self, year:int=1900, day:int=1, away_team:str='TeamKJ', home_team:str='TeamB') -> None:
        self.year = year
        self.day = day
        self.away_team = away_team
        self.home_team = home_team

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
    
    def get_statcast(self, play_id:int) -> Statcast:
        # get play_per_game and info
        events_play_id = self.game_events.X[self.game_events.X[:, 0] == play_id]
        play_per_game = events_play_id[0, 2]
        if play_per_game == play_id + 1: # some play occurred not tracked by play_id so decrease play_per_game by 1 to match
            play_per_game -= 1
        info_play_per_game = self.game_info.X[self.game_info.X[:, 3] == play_per_game]
        
        # if play_per_game not found increment until a match is found
        while len(info_play_per_game) == 0 and play_per_game < self.game_events.X[len(self.game_events.X) - 1, 2]:
            print('warning: play_id ' + str(play_id) + ' did not find a match for play_per_game ' + str(play_per_game) +
                  ' in game_info')
            play_per_game += 1
            info_play_per_game = self.game_info.X[self.game_info.X[:, 3] == play_per_game]
        
        if len(info_play_per_game) == 0: # end of game or error
            return None
        
        at_bat = info_play_per_game[0, 2]
        if at_bat == -1: # compute at bats
            at_bat = self.game_info.get_at_bats(play_per_game) # needs more testing

        inning = info_play_per_game[0, 4]
        inning_is_top = info_play_per_game[0, 5] > 0
        pitcher_id = info_play_per_game[0, 6]
        catcher_id = info_play_per_game[0, 7]
        firstbase_id = info_play_per_game[0, 8]
        secondbase_id = info_play_per_game[0, 9]
        thirdbase_id = info_play_per_game[0, 10]
        shortstop_id = info_play_per_game[0, 11]
        leftfield_id = info_play_per_game[0, 12]
        centerfield_id = info_play_per_game[0, 13]
        rightfield_id = info_play_per_game[0, 14]
        batter_id = info_play_per_game[0, 15]
        firstbase_runner_id = info_play_per_game[0, 16]
        secondbase_runner_id = info_play_per_game[0, 17]
        thirdbase_runner_id = info_play_per_game[0, 18]
        outs = self.get_outs(play_per_game, inning, inning_is_top) # needs more testing
        print('outs: ' + str(outs))
        pitch_count = self.game_info.get_pitch_count(play_per_game) # seems to work ok
        print('pitch count: ' + str(pitch_count))
        return info_play_per_game
    
    def get_outs(self, play_per_game:int, inning:int, inning_is_top:bool) -> int:
        inning_history = self.game_info.X[self.game_info.X[:, 3] <= play_per_game]
        inning_history = inning_history[inning_history[:, 4] == inning]
        inning_history = inning_history[(inning_history[:, 5] == 1) == inning_is_top]

        outs = 0
        i = 1
        prev_batter = inning_history[0, 15]
        while i < len(inning_history) and outs < 2:
            current_batter = inning_history[i, 15]
            if prev_batter != current_batter: # check if the previous batter advanced or hit a homerun
                if inning_history[i, 16] != prev_batter and inning_history[i, 17] != prev_batter and inning_history[i, 18] != prev_batter:
                    # the previous batter did not advance, but did they hit a home run?
                    game_events = self.game_events.X[self.game_events.X[:, 2] == inning_history[i - 1, 3]]
                    if len(game_events[game_events[:, 5] == 11]) == 0:
                        # the previous batter did not hit a home run, so they must be out
                        outs += 1
                prev_batter = current_batter
            i += 1
        return outs

class GameEvents:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = genfromtxt('./data/game_events/game_events' + table_suffix, skip_header=1, delimiter=',', dtype=None,
                            encoding=None, usecols=range(2, 8))
        if type(self.X[0][1]) == np.str_: # no at bat data so replace with -1
            for i in range(len(self.X)):
                self.X[i][1] = -1
            names = ['play_id','at_bat','play_per_game','timestamp','player_position','event_code']
            formats = ['i8', 'i8', 'i8', 'i8', 'i8', 'i8']
            self.X = self.X.astype(np.dtype({'names': names, 'formats': formats}))
            self.X = self.X.view((int, len(self.X.dtype.names)))

class GameInfo:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = genfromtxt('./data/game_info/game_info' + table_suffix, skip_header=1, delimiter=',', dtype=None,
                            encoding=None, usecols=range(2, 21))
        
        if type(self.X[0][2]) == np.str_: # no at bat data so replace with -1
            for i in range(len(self.X)):
                self.X[i][2] = -1

        for i in range(len(self.X)):
            self.X[i][0] = teams.index(self.X[i][0].strip('"'))
            self.X[i][1] = teams.index(self.X[i][1].strip('"'))
            if self.X[i][5].strip('"') == 'Top':
                self.X[i][5] = 1
            else:
                self.X[i][5] = 0

        names = ['home_team','away_team','at_bat','play_per_game','inning','top_bottom_inning','pitcher','catcher',
                'first_base','second_base','third_base','shortstop','left_field','center_field','right_field','batter',
                'first_baserunner','second_baserunner','third_baserunner']
        formats = ['i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8', 'i8']
        self.X = self.X.astype(np.dtype({'names': names, 'formats': formats}))
        self.X = self.X.view((int, len(self.X.dtype.names)))

    
    def get_at_bats(self, play_per_game:int) -> int:
        game_history = self.X[self.X[:, 3] <= play_per_game]
        batters = game_history[:, 15]
        return np.sum(batters[1:] != batters[:-1]) + 1 # number of times batter changes + 1 for initial batter
    
    def get_pitch_count(self, play_per_game:int) -> int:
        game_history = self.X[self.X[:, 3] <= play_per_game]
        pitcher_id = game_history[len(game_history) - 1, 6]
        pitcher_history = game_history[game_history[:, 6] == pitcher_id]
        # pitcher_play_per_game = pitcher_history[:, 3]
        # game_event_play_per_game = self.game_events.X[:, 2]
        # pitcher_events = self.game_events.X[np.isin(game_event_play_per_game, pitcher_play_per_game)]
        # pitch_count_1 = len(pitcher_events[pitcher_events[:, 5] == 1])
        return len(pitcher_history) - 1