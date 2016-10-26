"""
Helper functions for the analysis Module
"""


def single_file_output(in_file):
    """
    Extract sample name from file ie. /path/to/test.fa --> test
    :param in_file: path/to/file (str)
    :return: extracted sample name (str)
    """

    return in_file.split('/')[-1].split('.')[-2]


def cdp_file_output(in_seq_name1, in_seq_name2, ref, nt, ext):
    """
    Generate output file name
    :param in_seq_name1: sample name/s (str)
    :param in_seq_name2: sample name/s (str)
    :param ref: reference name (str)
    :param nt: aligned read length (int)
    :param ext: extension (ie. csv or pdf)
    :return: output filename (str)
    """
    file_name = "{0}_{1}_{2}_{3}.{4}".format(in_seq_name1,
                                             in_seq_name2,
                                             ref,
                                             nt,
                                             ext)
    if len(file_name) > 240:
        print("Auto-generated file name too long\n")
        file_name = "{0}_{1}.{2}".format(ref, nt, ext)
        print("{0} used instead\n".format(file_name))
    return file_name


def ref_seq_nt_output(in_seq_name, in_ref_name, nt, ext):
    """
    Generate output file name
    :param in_seq_name: treatment name (str)
    :param in_ref_name: reference name (str)
    :param nt: aligned read length (int)
    :param ext: extension (ie. csv or pdf)
    :return: output filename (str)
    """
    return "{0}_{1}_{2}.{3}".format(in_ref_name,
                                    in_seq_name,
                                    str(nt),
                                    ext)


def ref_seq_output(in_seq_name, in_ref_name, ext):
    """
    Generate output file name
    :param in_seq_name: treatment name (str)
    :param in_ref_name: reference name (str)nt)
    :param ext: extension (ie. csv or pdf)
    :return: output filename (str)
    """
    return "{0}_{1}.{2}".format(in_ref_name,
                                in_seq_name,
                                ext)
