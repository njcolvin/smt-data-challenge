from matplotlib.axes import Axes
import numpy as np

class BallPosition:

    def __init__(self, table_suffix:str) -> None:
        self.game_str = table_suffix.lstrip('-').rstrip('.csv')
        self.X = np.genfromtxt('./data/ball_pos/ball_pos' + table_suffix, skip_header=1,
                               delimiter=',', dtype=float, encoding=None, usecols=range(2, 7))

    def __plot2d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        ax.scatter(x, y, c='r', marker='o')

    def __plot3d__(self, play_id:int, ax:Axes):
        rows = self.X[self.X[:, 0] == play_id]
        x = rows[:, 2]
        y = rows[:, 3]
        z = rows[:, 4]
        ax.scatter(x, y, z, c='r', marker='o')

    """
    infield_bb computes and returns the list of infield batted ball positions

    :param hits: a np.ndarray of all the game events in plays where a hit occurred

    :return: a np.ndarray of ball positions throughout plays where infield hits occurred
    """
    def infield_bb(self, hits:np.ndarray):
        # TODO: determine slices, separate function
        angles = [-45 + (90/13 * i) for i in range(1, 13)] # for determining slices
        max_ts = 999999999 # timestamp
        dist_infield = 127.28125 # 127 feet 3 and 3/8 inches
        bb = []

        for play_id in np.unique(hits[:, 0]):
            rows = self.X[self.X[:, 0] == play_id]
            x = rows[:, 2]
            y = rows[:, 3]
            z = rows[:, 4]

            # if monotonically non-increasing then its foul, i think
            if not np.all(np.diff(y) <= 0):

                # check for first bounce/acquire
                bounces = hits[hits[:, 0] == play_id]
                bounces = bounces[bounces[:, 5] == 16]
                ts_bounce = max_ts
                if len(bounces) > 0:
                    ts_bounce = bounces[0, 3]
            
                acquired = hits[hits[:, 0] == play_id]
                acquired = acquired[acquired[:, 5] == 2]
                ts_acquired = max_ts
                if len(acquired) > 0:
                    ts_acquired = acquired[0, 3]
                
                if ts_acquired < max_ts or ts_bounce < max_ts: # if the ball didnt bounce and wasnt acquired, HR? 
                    # the earlier event represents when the ball first landed/was caught
                    ts = min([ts_bounce, ts_acquired])

                    # the closest timestamp should have a difference of 0 i.e. there's always a match
                    idx_bounce_acq = (np.abs(rows[:, 1] - ts)).argmin()

                    # the closest y-coordinate to the outfield defined by the line y = dist_infield
                    # TODO: better outfield definition i.e. circle instead of line
                    idx_pass_infield = (np.abs(y - dist_infield)).argmin()

                    # typically, idx_bounce_acq < idx_pass_infield -> ground ball rolled into outfield
                    #            idx_pass_infield < idx_bounce_acq -> fly ball into outfield
                    if y[idx_bounce_acq] > dist_infield:
                        # the ball passed the infield before bounce/acquire,
                        # was it still in the air from the hit and catchable?
                        if idx_pass_infield < idx_bounce_acq and z[idx_pass_infield] < 7:
                            # TODO: when determining slices, use idx_pass_infield as representative point?
                            bb.append([x, y, z])
                    else:
                        # the ball bounced/acquired within the infield
                        # if the ball never left the infield, it's an infield hit
                        if max(y) < dist_infield:
                            # TODO: when determining slices, use idx_bounce_acq as representative point?
                            bb.append([x, y, z])
                        elif idx_bounce_acq < idx_pass_infield:
                            # if the ball bounced/acquired before passing infield, it rolled or was thrown there
                            # TODO: when determining slices, use idx_bounce_acq as representative point?
                            bb.append([x, y, z])
                        # else, the ball passed the infield before bounce/acquire,
                        # but we just assumed it bounced/acquired within the infield.
                        # TODO: contradiction in infield_bb?

    # TODO: outfield_bb
    def outfield_bb(self, hits:np.ndarray):
        num_outfield = 0
        dist_infield = 127.28125

        for play_id in hits[:, 0]:
            rows = self.X[self.X[:, 0] == play_id]
            y = rows[:, 3]
            z = rows[:, 4]

            if max(y) > dist_infield:
                idx = (np.abs(y - dist_infield)).argmin()
                if z[idx] >= 7:
                    print('out')
                    num_outfield += 1