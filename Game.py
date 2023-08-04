import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.axes import Axes
from Ball import BallPosition
from Player import PlayerPosition
from Statcast import Statcast
from Glossary import teams

def field2d(ax:Axes):
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

def field3d(ax:Axes):
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

class GameData:

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
    
    def id_to_ppg(self, play_id:int) -> int:
        events_play_id = self.game_events.X[self.game_events.X[:, 0] == play_id]
        play_per_game = events_play_id[0, 2]
        if play_per_game == play_id + 1: # some play occurred not tracked by play_id so decrease play_per_game by 1 to match
            play_per_game -= 1
        return play_per_game
    
    def play_game_info(self, play_id:int) -> np.ndarray:
        play_per_game = self.id_to_ppg(play_id)
        info_play_per_game = self.game_info.X[self.game_info.X[:, 3] == play_per_game]

        # if play_per_game not found increment until a match is found
        while len(info_play_per_game) == 0 and play_per_game < self.game_events.X[len(self.game_events.X) - 1, 2]:
            print('warning: play_id ' + str(play_id) + ' did not find a match for play_per_game ' + str(play_per_game) +
                  ' in game_info')
            play_per_game += 1
            info_play_per_game = self.game_info.X[self.game_info.X[:, 3] == play_per_game]
        
        if len(info_play_per_game) == 0: # end of game or error
            return None
        
        return info_play_per_game

    def get_statcast(self, play_id:int) -> Statcast:
        # get play_per_game and info
        play_per_game = self.id_to_ppg(play_id)
        info_play_per_game = self.play_game_info(play_id)
        
        # get at bats
        at_bat = info_play_per_game[0, 2]
        print('at bat %d' % at_bat)
        if at_bat == -1:
            at_bat = self.game_info.at_bats(play_per_game) # TODO: at bats testing

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

        outs = self.get_outs(play_per_game, inning, inning_is_top) # TODO: outs testing
        
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
    
    def get_hit_events(self):
        hit_rows = self.game_events.X[self.game_events.X[:, 5] == 4]
        hit_events = []
        for play_id in hit_rows[:, 0]:
            play_rows = self.game_events.X[self.game_events.X[:, 0] == play_id]
            hit_events.extend(play_rows)
        return np.array(hit_events)
    

    def plot_play_2d(self, play_id:int):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot()
        field2d(ax)
        self.ball_pos.__plot2d__(play_id, ax)
        self.player_pos.__plot2d__(play_id, ax)
        plt.show()

    def plot_play_3d(self, play_id:int):
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(projection='3d')
        field3d(ax)
        self.ball_pos.__plot3d__(play_id, ax)
        self.player_pos.__plot3d__(play_id, ax)
        plt.title(play_id)
        plt.show()

    def infield_batted_balls(self):
        return self.ball_pos.infield_batted_balls(self.get_hit_events())

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

    def at_bats(self, play_per_game:int) -> int:
        game_history = self.X[self.X[:, 3] <= play_per_game]
        batters = game_history[:, 15]
        return np.sum(batters[1:] != batters[:-1]) + 1 # number of times batter changes + 1 for initial batter
    
    # TODO: finish pitch count
    def pitch_count(self, play_per_game:int) -> int:
        game_history = self.X[self.X[:, 3] <= play_per_game]
        pitcher_id = game_history[len(game_history) - 1, 6]
        pitcher_history = game_history[game_history[:, 6] == pitcher_id]
        # pitcher_play_per_game = pitcher_history[:, 3]
        # game_event_play_per_game = self.game_events.X[:, 2]
        # pitcher_events = self.game_events.X[np.isin(game_event_play_per_game, pitcher_play_per_game)]
        # pitch_count_1 = len(pitcher_events[pitcher_events[:, 5] == 1])
        return len(pitcher_history) - 1