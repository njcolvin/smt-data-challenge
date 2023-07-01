from numpy import genfromtxt

class TeamInfo:

    def __init__(self) -> None:
        self.X = genfromtxt('./data/team_info.csv', skip_header=1, delimiter=',', dtype=None, encoding=None)

    def get_roster(self, team_id:str, year:int) -> list:
        return [row for row in self.X if row[0] == 'Team' + team_id and row[2] == year]