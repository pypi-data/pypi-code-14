# coding=utf-8


import os, sys, re
from mimircache import *
from matplotlib import pyplot as plt


NUM_OF_THREADS = 48


def P3_aux():
    pass



def P3(dat):

    c = cachecow()
    # c.open("/home/jason/ALL_DATA/cloudphysics_txt_64K/{}.txt".format(dat), data_type='l')
    c.open("/home/jason/ALL_DATA/cloudphysics_fixed_blockSize/cloudphysics_parda_64KB_aligned_rw/txt/w{}.txt".format(dat), data_type='l')

    # c.vscsi("../mimircache/data/trace.vscsi")
    # n = c.reader.get_num_of_total_requests()
    nu = c.reader.get_num_of_unique_requests()
    cache_size = nu // 100
    bin_size = cache_size//NUM_OF_THREADS//2+2


    figname = "{}_LRU_Mithril.png".format(dat)


    c.plotHRCs(["LRU", "mimir", "FIFO", "mimir"],
                cache_params=[None,
                                {
                                "max_support": 15,
                                "min_support": 3,
                                "confidence": 0,
                                "item_set_size": 20,
                                "mining_period": 2000,
                                "prefetch_list_size": 2,
                                "mining_period_type": 'v',
                                "cache_type": "LRU",
                                "sequential_type":0,
                                "max_metadata_size": 0.2,
                                "block_size":64*1024,
                                "sequential_K":0,
                                "cycle_time":2,
                               },
                              None,
                              {
                                  "max_support": 15,
                                  "min_support": 3,
                                  "confidence": 0,
                                  "item_set_size": 20,
                                  "mining_period": 2000,
                                  "prefetch_list_size": 2,
                                  "mining_period_type": 'v',
                                  "cache_type": "FIFO",
                                  "sequential_type": 0,
                                  "max_metadata_size": 0.2,
                                  "block_size": 64 * 1024,
                                  "sequential_K": 0,
                                  "cycle_time": 2,
                              }
                              ],
               cache_size=cache_size, bin_size=bin_size,
               auto_size=False, num_of_threads=NUM_OF_THREADS,
               label=["LRU", "Mithril-LRU", "FIFO", "Mithril-FIFO"], figname=figname)


    figname = "{}_AMP_Mithril.png".format(dat)
    c.plotMRCs(["AMP", "mimir"],
               cache_params=[{"APT": 4, "read_size": 1},
                             {
                             "max_support": 15,
                             "min_support": 3,
                             "confidence": 0,
                             "item_set_size": 20,
                             "mining_period": 2000,
                             "prefetch_list_size": 2,
                             "mining_period_type": 'v',
                             "cache_type": "LRU",
                             "sequential_type": 1,
                             "max_metadata_size": 0.2,
                             "block_size": 64 * 1024,
                             "sequential_K": 2,
                             "cycle_time": 2,
                             }],
               cache_size=cache_size, bin_size=bin_size,
               auto_size=False, num_of_threads=NUM_OF_THREADS,
               figname=figname)


if __name__ == "__main__":
    for i in range(106, 0, -1):
        P3("w{}".format(i))