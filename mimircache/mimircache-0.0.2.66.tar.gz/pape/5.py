import os, sys, time, pickle
sys.path.append("../")

from mimircache import *
import mimircache.c_generalProfiler as c_generalProfiler
import concurrent.futures
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def get_HR_PE(dat, d):
    # reader = plainReader("/home/jason/ALL_DATA/cloudphysics_txt_64K/w{}.txt".format(dat), data_type='l')
    # reader = plainReader("/media/jason/LinuxData/cloudphysics_txt_64K/w{}.txt".format(dat), data_type='l')
    reader = plainReader("/home/jason/ALL_DATA/cloudphysics_fixed_blockSize/cloudphysics_parda_64KB_aligned_rw/txt/w{}.txt".format(dat), data_type='l')
    # reader = plainReader("../mimircache/data/trace.txt", data_type='l')

    n = reader.get_num_of_total_requests()
    nu = reader.get_num_of_unique_requests()
    print("{}: total {}, uniq {}".format(dat, n, nu))
    CACHE_SIZE = nu//100
    r = c_generalProfiler.get_HR_PE(reader=reader.cReader, cache_size=CACHE_SIZE)
    d[dat] = r
    return r, n, nu


def get_HR_PE_thread(dat):
    # if dat<10:
    #     dat = '0' + str(dat)
    # reader = plainReader("/home/jason/ALL_DATA/cloudphysics_txt_64K/w{}.txt".format(dat), data_type='l')
    reader = plainReader("/home/jason/ALL_DATA/msr_fixed_blockSize/msr_parda_64KB_aligned_rw/txt/{}".format(dat), data_type='l')
    # reader = plainReader("/home/jason/ALL_DATA/cloudphysics_fixed_blockSize/cloudphysics_parda_64KB_aligned_rw/txt/w{}.txt".format(dat), data_type='l')
    # reader = plainReader("../mimircache/data/trace.txt", data_type='l')

    n = reader.get_num_of_total_requests()
    nu = reader.get_num_of_unique_requests()
    print("{}: total {}, uniq {}".format(dat, n, nu))
    CACHE_SIZE = nu//100
    r = c_generalProfiler.get_HR_PE(reader=reader.cReader, cache_size=CACHE_SIZE)
    return r, n, nu


def get_HR_PE_main_thread():
    AMP_n = 8
    mithril_n1 = 12

    d = {}
    f = open("r_MSR", 'w')
    # file_list = os.listdir("/home/jason/ALL_DATA/msr_fixed_blockSize/msr_parda_64KB_aligned_rw/txt")


    max_process = int(multiprocessing.cpu_count()//4*1.2)
    print("using {} processes".format(max_process))
    with ProcessPoolExecutor(max_workers=max_process) as e:
        # submit_result = {e.submit(get_HR_PE_thread, i):i for i in range(106, 0, -1)}
        # submit_result = {e.submit(get_HR_PE_thread, i):i for i in range(106, 1, -1)}
        submit_result = {e.submit(get_HR_PE_thread, f):f
                         for f in os.listdir("/home/jason/ALL_DATA/msr_fixed_blockSize/msr_parda_64KB_aligned_rw/txt/")}

        print("all tasks submitted")
        while len(submit_result):
            to_del = []
            for future, order in submit_result.items():
                if future.done():
                    r, n, nu = future.result()
                    d[order] = r
                    f2 = open("r_MSR.pickle", 'wb')
                    pickle.dump(d, f2)
                    f2.close()
                    f.write("{}: total {}, unique {}\n".format(order, n, nu))
                    for i in range(len(r) // 4):
                        real_num = i
                        if real_num > AMP_n:
                            real_num -= AMP_n+1
                        if i == 1:
                            f.write("AMP:\n")
                        if i == AMP_n+1:
                            f.write("mimir:\n")
                        # if i == 1 + AMP_n + mithril_n1:
                        #     f.write("mimir+AMP:\n")
                        f.write("{:2d}: {:.5f}, {:.5f}({}, {})\n".format(real_num, r[i * 4 + 2], r[i * 4 + 3], int(r[i * 4]),
                                                                         int(r[i * 4 + 1])))
                    f.write("\n\n")
                    f.flush()
                    to_del.append(future)
            # else:
            #     print("no finished")
            for future in to_del:
                del submit_result[future]

            time.sleep(20)
            # print("done sleep")
    f.close()



if __name__ == "__main__":
    import time

    get_HR_PE_main_thread()


    # AMP_n = 8
    # mithril_n1 = 12
    #
    # d = {}
    # f = open("r", 'w')
    # f2 = open("r.pickle", 'wb')
    # # for dat in range(90, 89, -1):
    # for dat in range(106, 1, -1):
    #     r, n, nu = get_HR_PE(dat, d)
    #     f.write("w{}: total {}, unique {}\n".format(dat, n, nu))
    #     for i in range(len(r) // 4):
    #         real_num = i
    #         if real_num > AMP_n:
    #             real_num -= AMP_n + 1
    #         if i == 1:
    #             f.write("AMP:\n")
    #         if i == AMP_n + 1:
    #             f.write("mimir:\n")
    #         if i == 1 + AMP_n + mithril_n1:
    #             f.write("mimir+AMP:\n")
    #         f.write("{:2d}: {:.5f}, {:.5f}({}, {})\n".format(real_num, r[i * 4 + 2], r[i * 4 + 3], int(r[i * 4]),
    #                                                          int(r[i * 4 + 1])))
    #     f.write("\n\n")
    #     f.flush()
    # pickle.dump(d, f2)


