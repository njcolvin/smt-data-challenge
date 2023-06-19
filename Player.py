from numpy import genfromtxt

class PlayerPosition:

    def __init__(self, filename:str) -> None:
        self.X = genfromtxt(filename, skip_header=1, delimiter=',', dtype=None, encoding=None)