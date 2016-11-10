

import os, time
from mimircache import *





MINING_PERIOD1       = 5000
PREFETCH_TABLE1      = 30000
PREFETCH_LIST_SIZE1  = 2


MINING_PERIOD2       = 5000
PREFETCH_TABLE2      = 80000
PREFETCH_LIST_SIZE2  = 2





def get_r1(dat):
    result = []


    # reader = plainReader("/scratch/jason/msr_parda_64KB_aligned_rw/txt/{}".format(dat), data_type='l')
    reader = plainReader("/home/jason/ALL_DATA/cloudphysics_txt_64K/w{}.txt".format(dat), data_type='l')

    # r = vscsiReader(dat, data_type='l')
    n = reader.get_num_of_total_requests()
    nu = reader.get_num_of_unique_requests()
    print("{}: total {}, uniq {}".format(dat, n, nu))
    CACHE_SIZE = nu//100
    BIN_SIZE = CACHE_SIZE
    COMPENSATE1 = 14*4        # 225
    COMPENSATE2 = 16
    COMPENSATE2 = int( ((8 + 8 + 8 * 3) * MINING_PERIOD2 + (8 + 8 * 2) * (0.02*nu)) / (16*1024))


    lp = LRUProfiler(reader)
    mr_LRU = lp.get_miss_rate()
    result.append(mr_LRU[CACHE_SIZE])

    cg_AMP = cGeneralProfiler(reader, "AMP",
                              CACHE_SIZE,
                              BIN_SIZE,
                              cache_params={"APT":4, "read_size":1},
                              num_of_threads=1)
    mr_AMP = cg_AMP.get_miss_rate()
    result.append(mr_AMP[1])


    cg_Mithril0 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 8,
                                                 "min_support": 1,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type":0,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M0 = cg_Mithril0.get_miss_rate()
    result.append(mr_M0[1])



    cg_Mithril1 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 10,
                                                 "min_support": 2,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type":0,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M1 = cg_Mithril1.get_miss_rate()
    result.append(mr_M1[1])


    cg_Mithril2 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 20,
                                                 "min_support": 4,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type":0,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M2 = cg_Mithril2.get_miss_rate()
    result.append(mr_M2[1])


    cg_Mithril3 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 30,
                                                 "min_support": 6,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type":0,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M3 = cg_Mithril3.get_miss_rate()
    result.append(mr_M3[1])




    cg_Mithril4 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 20,
                                                 "min_support": 4,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 1,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M4 = cg_Mithril4.get_miss_rate()
    result.append(mr_M4[1])

    cg_Mithril5 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 30,
                                                 "min_support": 6,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "LRU",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 1,
                                                 "sequential_K": 2,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M5 = cg_Mithril5.get_miss_rate()
    result.append(mr_M5[1])


    cg_Mithril6 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 10,
                                                 "min_support": 2,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "AMP",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 2,
                                                 "sequential_K": 0,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M6 = cg_Mithril6.get_miss_rate()
    result.append(mr_M6[1])

    cg_Mithril7 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 20,
                                                 "min_support": 3,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "AMP",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 2,
                                                 "sequential_K": 0,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M7 = cg_Mithril7.get_miss_rate()
    result.append(mr_M7[1])

    cg_Mithril8 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 20,
                                                 "min_support": 4,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "AMP",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 2,
                                                 "sequential_K": 0,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M8 = cg_Mithril8.get_miss_rate()
    result.append(mr_M8[1])


    cg_Mithril9 = cGeneralProfiler(reader, "mimir",
                                   CACHE_SIZE,
                                   BIN_SIZE,
                                   cache_params={"max_support": 30,
                                                 "min_support": 6,
                                                 "confidence": 0,
                                                 "item_set_size": 20,
                                                 "prefetch_list_size": PREFETCH_LIST_SIZE1,
                                                 "cache_type": "AMP",
                                                 "mining_period_type": 'v',
                                                 "sequential_type": 2,
                                                 "sequential_K": 0,
                                                 "max_metadata_size": 0.2,
                                                 "block_size": 64 * 1024,
                                                 "cycle_time": 2,
                                                 },
                                   num_of_threads=1)
    mr_M9 = cg_Mithril9.get_miss_rate()
    result.append(mr_M9[1])

    return result


# def run_for_traces(reader):
#     n = reader.num_
#     p = cGeneralProfiler(reader, 'AMP', CACHE_SIZE, BIN_SIZE, num_of_threads=NUM_OF_THREADS)



if __name__ == "__main__":
    # reader = vscsiReader("../data/trace.vscsi")
    # f = '../mimircache/data/trace.vscsi'
    # for f in os.listdir("/scratch/jason/msr_parda_64KB_aligned_rw/txt"):
    import time
    # time.sleep(3600)
    for f in range(106, 0, -1):
        # print(f)
        r = get_r1(f)
        print("w{}: {}".format(f, r))