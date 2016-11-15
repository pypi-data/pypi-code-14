from matplotlib.ticker import MaxNLocator

from mimircache import *
import re, os, sys
import pickle
import numpy as np
from matplotlib import pyplot as plt



MATPLOTLIB_COLORS  = ["b", "r", "c", "g", "m", "y", "k"]
MATPLOTLIB_MARKERS = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd']


def P1_aux(dat):
    current_dat = None
    d = {}

    regex_LRU = re.compile(r" 0: (?P<HR>0.\d+), (?P<PE>0.\d+)\((?P<size>\d+), (?P<prefetch>\d+)\)")
    regex_AMP = re.compile(r" 1: (?P<HR>0.\d+), (?P<PE>0.\d+)\((?P<size>\d+), (?P<prefetch>\d+)\)")
    regex_general = re.compile(r"\s{0,1}(?P<num>\d+): (?P<HR>0.\d+), (?P<PE>0.\d+)\((?P<size>\d+), (?P<prefetch>\d+)\)")

    with open(dat) as ifile:
        for line in ifile:
            if line.startswith("w"):
                current_dat = line[:line.find(":")]
                LRU_MR = 0
                LRU_PE = 0
                AMP_MR = 0
                AMP_PE = 0
                Mithril1_MR = 0
                Mithril1_PE = 0
                Mithril2_MR = 0
                Mithril2_PE = 0
                continue
            m = regex_AMP.match(line)
            if m:
                AMP_MR = 1 - float(m.group("HR"))
                AMP_PE = m.group("PE")
                continue
            m = regex_LRU.match(line)
            if m:
                LRU_MR = 1 - float(m.group("HR"))
                LRU_PE = m.group("PE")
                continue
            m = regex_general.match(line)
            if m:
                num = int(m.group("num"))
                if num <= 9:
                    Mithril1_MR = 1 - float(m.group("HR"))
                    Mithril1_PE = m.group("PE")
                    continue
                else:
                    Mithril2_MR = 1 - float(m.group("HR"))
                    Mithril2_PE = m.group("PE")
                    # d[current_dat] = [[LRU_MR, AMP_MR, Mithril1_MR, Mithril2_MR],
                    #                   [AMP_PE, AMP_PE, Mithril1_PE, Mithril2_PE]]
                    d[current_dat] = [[LRU_MR, AMP_MR, Mithril2_MR],
                                      [AMP_PE, AMP_PE, Mithril2_PE]]

        with open("dat.pickle", 'wb') as ofile:
            pickle.dump(d, ofile)

        return d

def P1(dat):
    cache_alg = ["LRU", "AMP", "Mithril"]
    n_cache = 0

    d = P1_aux(dat)
    print("{}: {}".format(len(d), sorted(d.items())))
    count = 0
    ncolumn = len(d)//3
    if ncolumn * 3 < len(d):
        ncolumn += 1

    f, axs = plt.subplots(3, ncolumn, sharex=True, sharey=True, figsize=(20, 8))


    ax = f.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axes
    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    ax.set_xlabel("hit rate")
    ax.set_ylabel("prefetch efficiency")


    for k,v in sorted(d.items()):
        n_cache = len(v[0])
        for i in range(len(v[0])):
            axs[count//ncolumn][count%ncolumn].plot(1 - v[0][i], v[1][i], "{}{}-".format(
                MATPLOTLIB_COLORS[i%len(MATPLOTLIB_COLORS)],
                MATPLOTLIB_MARKERS[i%len(MATPLOTLIB_MARKERS)]),
                label=cache_alg[i], markersize=12)
        # plt.plot(v[0][1], v[1][1], "bs-", markersize=8)
        # plt.plot(v[0][2], v[1][2], "cp-", markersize=12)
        # plt.plot(v[0][3], v[1][3], "m*-", markersize=12)
        # plt.plot([v[0][0], v[0][1]], [v[1][0], v[1][1]], linestyle='-', linewidth=2)
        axs[count//ncolumn][count%ncolumn].plot(np.array(v[0])*-1+1, v[1], linestyle='-', linewidth=2)
        count += 1

    f.subplots_adjust(wspace=0, hspace=0.12)

    handles = [plt.Line2D((0, 1), (0, 0), color=MATPLOTLIB_COLORS[i],
                          marker=MATPLOTLIB_MARKERS[i], linestyle='') for i in range(n_cache)]
    plt.figlegend(handles, cache_alg, 'lower right')

    plt.gca().yaxis.set_major_locator(MaxNLocator(prune='lower'))
    # axs[-1][-1].set_ylim(ymin=0.6, ymax=1)
    axs[-1][-1].yaxis.set_ticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    for i in range(ncolumn):
        axs[-1][i].set_xlim(xmin=0, xmax=1)
        axs[-1][i].xaxis.set_ticks([0, 0.5])

    plt.setp([a.get_xticklabels() for a in f.axes[:-ncolumn-1]], visible=False)



    plt.savefig("P1.png", dpi=200)


if __name__ == "__main__":
    P1("dat")



