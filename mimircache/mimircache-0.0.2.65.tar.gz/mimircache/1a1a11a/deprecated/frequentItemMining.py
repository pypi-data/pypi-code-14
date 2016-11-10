import os
import shutil
from mimircache.profiler.twoDPlots import *

THRESHOLD_HIGH = 100
THRESHOLD_LOW = 10
# TIME_INTERVAL = 100000


def generate_itemset(file_loc, time_interval):
    whole_data_set = []
    folder_name = file_loc[file_loc.rfind('/')+1:]
    folder_name = folder_name.split('_')[0]+'Mining'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    reader = vscsiReader(file_loc)
    bp = cHeatmap().gen_breakpoints(reader, 'r', time_interval)
    print(len(bp))
    # print(bp)
    bp_len = [bp[i] - bp[i - 1] for i in range(1, len(bp), 1)]
    print("max length: {}".format(max(bp_len)))
    count_high = 0
    count_low = 0
    for i in range(len(bp_len)):
        if bp_len[i] > THRESHOLD_HIGH:
            count_high += 1
        if bp_len[i] < THRESHOLD_LOW:
            count_low += 1

    print(">{} : {}, <{}: {}".format(THRESHOLD_HIGH, count_high, THRESHOLD_LOW, count_low))
    order = 1
    item_set = set()
    for num, item in enumerate(reader):
        item_set.add(str(item))
        if num == bp[order]:
            # if len(item_set)>THRESHOLD_LOW:
            whole_data_set.append(item_set)
            item_set = {str(item)}
            order += 1
    whole_data_set.append(item_set)

    # print(whole_data_set[-1])
    print(len(whole_data_set))

    with open(folder_name+'/'+'all_itemset_{}.part1'.format(time_interval), 'w') as ofile1:
        with open(folder_name + '/' + 'all_itemset_{}.part2'.format(time_interval), 'w') as ofile2:
            with open(folder_name + '/' + 'all_itemset_{}.part3'.format(time_interval), 'w') as ofile3:
                for i in range(len(whole_data_set)):
                    item_set = whole_data_set[i]
                    if i<len(whole_data_set)/3:
                        ofile1.write(' '.join(item_set) + '\n')
                    elif i<len(whole_data_set)/3*2:
                        ofile2.write(' '.join(item_set) + '\n')
                    else:
                        ofile3.write(' '.join(item_set) + '\n')


def generate_itemset_logical(file_loc, time_interval):
    r = vscsiReader(file_loc)
    count = 0
    with open(file_loc+'.itemset_logical_{}'.format(time_interval), 'w') as ofile:
        for request in r:
            ofile.write("{} ".format(request))
            count += 1
            if count == time_interval:
                ofile.write('\n')
                count = 0




def test2(dat1, dat2):
    item_set1 = set()
    item_set2 = set()
    with open(dat1, 'r') as ifile1:
        for line in ifile1:
            item_set1.add(frozenset(line[:line.index('#')].split()))

    with open(dat2, 'r') as ifile2:
        for line in ifile2:
            item_set2.add(frozenset(line[:line.index('#')].split()))

    # print(item_set1)
    print("item set1 size: {}, item set2 size: {}, item_set1 - item_set2 size: {}".format(
        len(item_set1), len(item_set2), len(item_set1 - item_set2)))


def convert_format(dat):
    d = {}
    with open(dat) as ifile:
        for line in ifile:
            line = line[:line.find('#')].strip().split()
            for item1 in line:
                for item2 in line:
                    if item1 in d:
                        d[item1].add(item2)
                    else:
                        d[item1] = {item2}
    with open(dat + '.converted', 'w') as ofile:
        for key, value in d.items():
            ofile.write(key + '\t')
            for i in value:
                ofile.write(i + '\t')
            ofile.write('\n')
    shutil.copy(dat + '.converted', "../profiler/frequentItemSet")


if __name__ == "__main__":
    # test1("../data/trace.vscsi")
    # generate_itemset("../data/traces/w106_vscsi1.vscsitrace")
    generate_itemset("w38NewMining/w38_vscsi1.vscsitrace", 1000)
    # test2('test', 'test2')

    # convert_format('w106Mining/out.part1')
