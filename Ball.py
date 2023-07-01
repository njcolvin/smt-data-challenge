from numpy import genfromtxt

class BallPosition:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = genfromtxt('./data/ball_pos/ball_pos' + table_suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)