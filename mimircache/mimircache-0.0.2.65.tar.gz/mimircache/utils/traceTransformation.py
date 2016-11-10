

import os
from mimircache import vscsiReader



def vReaderToPReader(file_path, output_path):
    vReader = vscsiReader(file_path)
    with open(output_path, 'w') as ofile:
        for req in vReader:
            ofile.write("{}\n".format(req))

def vReaderTocsvReader(file_pth, output_path):
    pass


def splitTrace(reader, n, output_folder, prefix=""):
    """
    given a reader, split the content into n small files
    :param reader:
    :param n:
    :param output_folder:
    :param prefix:
    :return:
    """
    total_num = reader.get_num_of_total_requests()
    num_each_file = total_num // n
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    ofiles = []
    for i in range(n):
        ofiles.append(open("{}/{}".format(output_folder, prefix+str(i)), 'w'))
    file_p = -1
    for i, e in enumerate(reader):
        if i % num_each_file == 0 and file_p!=len(ofiles)-1:
            file_p += 1
        ofiles[file_p].write("{}\n".format(e))

    for i in range(n):
        ofiles[i].close()


def trace_mixer(reader1, reader2, mix_mode, output="mixTrace.txt", *args, **kwargs):
    """
    mix two traces into one,
    :param reader1:
    :param reader2:
    :param mix_mode: "real_time", "round_robin"
    :return:
    """
    ofile = open(output, 'w')
    if mix_mode == "round_robin":
        if "round_robin_n" in kwargs:
            round_robin_n = kwargs["round_robin_n"]
        else:
            round_robin_n = 1
        begin_flag = True
        r1 = None
        r2 = None

        while begin_flag or r1 or r2:
            if begin_flag or r1:
                for i in range(round_robin_n):
                    r1 = reader1.read_one_element()
                    if r1:
                        ofile.write("{}\n".format(r1))
                    else:
                        break
            if begin_flag or r2:
                for i in range(round_robin_n):
                    r2 = reader2.read_one_element()
                    if r2:
                        ofile.write("{}\n".format(r2))
                    else:
                        break

            begin_flag = False



    elif mix_mode == "real_time":
        r1 = reader1.read_time_request()
        r2 = reader2.read_time_request()
        init_t1 = r1[0]
        init_t2 = r2[0]
        while r1 or r2:
            if r1[0] - init_t1 <= r2[0] - init_t2:
                ofile.write("{}\n".format(r1[1]))
                r1 = reader1.read_time_request()
            else:
                ofile.write("{}\n".format(r2[1]))
                r2 = reader2.read_time_request()
            if not r1:
                while r2:
                    ofile.write("{}\n".format(r2[1]))
                    r2 = reader2.read_time_request()
            if not r2:
                while r1:
                    ofile.write("{}\n".format(r1[1]))
                    r1 = reader1.read_time_request()


    else:
        print("do not support given mix mode {}".format(mix_mode), file=sys.stderr)


    ofile.close()


if __name__ == "__main__":
    import sys
    # vReaderToPReader(sys.argv[1], sys.argv[2])
    # reader = vscsiReader("../data/traces/w38_vscsi1.vscsitrace")
    reader1 = vscsiReader("../data/trace.vscsi")
    reader2 = vscsiReader("../data/traces/w100_vscsi1.vscsitrace")
    # trace_mixer(reader1, reader2, mix_mode="round_robin", round_robin_n=2)
    trace_mixer(reader1, reader2, mix_mode="real_time")
    # splitTrace(reader, 2, "w38Split")
