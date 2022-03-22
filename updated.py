"""first aircraft to be the resolved_unmaneuvered, second will be the unresolved and third will be the predicted"""

from buttons import Button


class aircraft():
    def __init__(self, df):
        self.exe_traj = []
        self.org_traj = [df['longitude'], df['latitude']]
        self.res_traj = []
        self.Nsteps = 0
        self.offset = 0
        self.start_time = 0


dir_res = 'resolved_initial/'
dir_unres = 'unres_initial/'
dir_pred = 'predicted_trajs/'

sorted_resdir = sorted(os.listdir(
    dir_res), key=lambda x: int(x.split('.')[0][15:]))
sorted_unresdir = sorted(os.listdir(dir_unres),
                         key=lambda x: int(x.split('.')[0][15:]))
sorted_preddir = sorted(os.listdir(dir_pred),
                        key=lambda x: int(x.split('.')[0][15:]))


def trimming():
    return 0


aircraftsets = [] < -- from data  # this is the set of aircrafts in one scenario
for i in range(len(sorted_resdir)):


get the min_start_time - -> calculate the offset: for i in range(len(a)): a[i].offset = a[i].start_time - min_start_time


trimming(a):
    min_length = 10000
    for j in range(len(a)):
        min_length > len(a[j].org_traj) + a[j].offset
        min_length > len(a[j].res_traj) + a[j].offset


for i in range(0, min_length):

    plot Background
    plot position
    for j in range(len(a)):
        if i > a[j].offset:
            plot(a[j].exe_traj[i])

    plot button:
    if a[1].offset <= i <= (a[1].Nsteps - a[1].offset):
        if accepted and (not res_acceptance):
            res_acceptance = True
            a[1].exe_traj = a[1].res_traj


mai_simulation()
