event_code = {
    1 : 'pitch',
    2 : 'ball acquired',
    3 : 'throw (ball-in-play)',
    4 : 'ball hit into play',
    5 : 'end of play',
    6 : 'pickoff throw',
    7 : 'ball acquired - unknown field position',
    8 : 'throw (ball-in-play) - unknown field position',
    9 : 'ball deflection',
    10 : 'ball deflection off of wall',
    11 : 'home run',
    16 : 'ball bounce'
}

player_position = {
    1 : 'pitcher',
    2 : 'catcher',
    3 : 'first baseman',
    4 : 'second baseman',
    5 : 'third baseman',
    6 : 'shortstop',
    7 : 'left field',
    8 : 'center field',
    9 : 'right field',
    10 : 'batter',
    11 : 'runner on first base',
    12 : 'runner on second base',
    13 : 'runner on third base',
    255 : 'ball event with no player (e.g., ball bounce)'
}

bb_type = {
    1 : 'ground_ball',
    2 : 'line_drive',
    3 : 'fly_ball',
    4 : 'popup'
}

# use the index as an encoded label
teams = ['TeamA1', 'TeamA2', 'TeamA3', 'TeamB', 'TeamKJ', 'TeamKK', 'TeamKL', 'TeamLG', 'TeamLI', 'TeamLK', 'TeamLJ', 'TeamLL', 'TeamLH', 'TeamMG',
        'TeamML', 'TeamMJ', 'TeamMI', 'TeamMD', 'TeamMK', 'TeamMB', 'TeamME', 'TeamMA', 'TeamMH', 'TeamMC', 'TeamMF', 'TeamNE', 'TeamNC', 'TeamND',
        'TeamNJ', 'TeamNG', 'TeamNI', 'TeamNL', 'TeamNA', 'TeamNH', 'TeamNK', 'TeamNF', 'TeamNB']