#!/usr/bin/env python

import profile_plotter as prp
import sys
import time

# global defaults
n_out_def = 1
data_dir_def = './'


def plot_snapshots(n_out=n_out_def, data_dir=data_dir_def):

    for i in range(n_out + 1)[:]:
        prp.plot_snapshot(i, data_dir)


if __name__ == '__main__':

    assert(len(sys.argv) in [3, 4])

    if len(sys.argv) == 4:
        time.sleep(int(sys.argv[3]))

    plot_snapshots(int(sys.argv[1]), sys.argv[2])
