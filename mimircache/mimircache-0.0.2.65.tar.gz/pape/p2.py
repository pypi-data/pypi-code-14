# coding=utf-8


import os, sys, re
from mimircache import *
from matplotlib import pyplot as plt





def P2_aux(dat):
    regex_AMP = re.compile(r"cache size (?P<cache_size>\d+), hit rate (?P<HR>0.\d+), prefetch \d+, hit \d+, accuracy: (?P<PE>0.\d+)")
    regex_Mithril = re.compile(r"overall size (?P<cache_size>\d+), hit rate (?P<HR>0.\d+), efficiency (?P<PE>0.\d+)")

    result = {"AMP":[], "Mithril":[]}
    with open(dat) as ifile:
        for line in ifile:
            m = regex_AMP.match(line)
            if m:
                result["AMP"].append((m.group("HR"), m.group("PE")))
                continue
            m = regex_Mithril.match(line)
            if m:
                result["Mithril"].append((m.group("HR"), m.group("PE")))
                continue
    return result




def P2(dat):
    d = P2_aux(dat)
    print(d)

    x = [float(x) for (x, y) in sorted(d["AMP"])]
    y = [y for (x, y) in sorted(d["AMP"])]
    plt.plot(x, y, color='r', marker='o', ls='-', label="AMP")

    x = [float(x) for (x, y) in sorted(d["Mithril"])]
    y = [y for (x, y) in sorted(d["Mithril"])]
    plt.plot(x, y, color='c', marker='s', ls='--', label="Mithril")
    plt.xlabel("hit rate")
    plt.ylabel("prefetch efficiency")
    plt.legend(loc="best")

    plt.savefig("P2_{}.png".format(dat[dat.rfind('.')+1:]), dpi=600)



if __name__ == "__main__":
    P2("../mimircache/profiler/cG.out.w60")
