from numpy import genfromtxt

class BallPosition:

    def __init__(self, suffix:str) -> None:
        self.X = genfromtxt('./data/ball_pos/ball_pos' + suffix, skip_header=1, delimiter=',', dtype=None, encoding=None)