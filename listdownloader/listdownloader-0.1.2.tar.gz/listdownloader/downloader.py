import urllib
import urllib.request
import urllib.error
import os
import sys
import hashlib
import random
import datetime
import multiprocessing as mp
import errno
import re

random.seed(datetime.datetime.now())


def mkdir_p(path):
    """
    Create directory incrementally whether and don't raise if it exists
    :param path: directory path
    :return: None
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def md5_file(file_name):
    """
    Calculate md5 of a file
    :param file_name: path of the file, for which md5 to be calculated
    :return: md5 string
    """
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_random_hash(bits=32):
    """
    Create a random hash that with "bits" length
    :param bits: number of bits of the hash
    :return: the hash value
    """
    assert bits % 8 == 0
    required_length = bits / 8 * 2
    s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
    if len(s) < required_length:
        return get_random_hash(bits)
    else:
        return s


def files_are_same(file1, file2):
    """
    Checks whether two files in two paths are the same.
    First by checking their sizes. If the sizes are equal, an MD5 checksum is calculated.
    :param file1: first file
    :param file2: second file
    :return: True if files are the same, False otherwise
    """
    if file1 == file2:
        return True

    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    if size1 != size2:
        return False

    else:
        md5file1 = md5_file(file1)
        md5file2 = md5_file(file2)
        return md5file1 == md5file2


def rename_file_with_number(file_name, num):
    """
    Returns the same file name, but with a number added.
    myfile.doc becomes myfile_1.doc or myfile_num.doc
    :param file_name: file to be renamed
    :param num: number to add to filename
    :return: renamed file name
    """
    file_name_parts = file_name.split(".")
    return "".join(file_name_parts[0:-1]) + "_" + str(num) + "." + file_name_parts[-1]


def download_file(url, to_dir):

    """
    A function that downloads a file to a specific directory.
    If the file already exists, it tries to add a number to the file name.
    If the same file exists, the file is not downloaded again.
    The check whether it's the same file is done through file size and md5 checksum
    :param url: url of the file to be downloaded
    :param to_dir: directory, to which the file should be downloaded
    :return: None
    """

    file_name = os.path.normpath(url.split('/')[-1]).replace(" ","")
    file_name = re.sub('[^\w_.)( -]', '', file_name) # remove invalid characters from filename
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            info = response.info()
            ext = info.get_content_subtype()
            if len(file_name) < len(ext) or file_name[-len(ext):] != ext: # add file extension if not present
                file_name += "." + ext
    except urllib.error.URLError as e:
        sys.stderr.write("Skipping invalid URL, or possibly failed to get URL: " + url + "\nError message: " + str(e))
        return

    target_path = os.path.join(to_dir, file_name)
    target_temp_path = os.path.join(to_dir, file_name + "_" + get_random_hash())

    with open(target_temp_path, 'wb') as f:
        f.write(data)

    # check if a file with the same name exists already
    if os.path.isfile(target_path):
        # if file exists, compare with the downloaded file
        if files_are_same(target_path, target_temp_path):
            # if it's the same file, just remove the temp file and return
            os.remove(target_temp_path)
            return
        else:
            # if it's not the same file, loop over new file names with numbers, and redo the file name check
            idx = 0
            while True:
                idx += 1
                num_file_name = rename_file_with_number(file_name, idx)
                target_path = os.path.join(to_dir, num_file_name)
                if os.path.isfile(target_path):
                    if files_are_same(target_path, target_temp_path):
                        os.remove(target_temp_path)
                        return
                else:
                    break

    # if the downloaded file will not overwrite anything, rename the temp file to its proper name
    os.rename(target_temp_path, target_path)


def _download_files(list_of_urls, to_dir):
    """
    Download list of urls to a directory sequentially
    :param list_of_urls: list of urls to download
    :param to_dir: destination directory
    :return: None
    """
    for url in list_of_urls:
        download_file(url, to_dir)


def download_files(list_of_urls, to_dir, processes=0):
    """
    Downloads a list of urls in parallel if possible, otherwise sequentially
    :param list_of_urls: list of urls to download
    :param to_dir: destination directory
    :param processes: number of processes/threads
    :return: None
    """

    # clean spaces, tabs and new-lines
    list_of_urls = [line.replace(' ', '').replace('\n', '').replace('\t', '') for line in list_of_urls]
    if not os.path.isdir(to_dir):
        mkdir_p(to_dir)
    if processes <= 0:
        try:
            processes = mp.cpu_count()
        except NotImplementedError as e:
            sys.stderr.write("Unable to determine the number of CPUs for parallelization. Proceeding sequentially. "
                             "Consider inputting the number of CPUs manually.\n")
            _download_files(list_of_urls, to_dir)
            return
    elif processes == 1 or len(list_of_urls) == 1:
        _download_files(list_of_urls, to_dir)
        return
    elif processes > len(list_of_urls):
        processes = len(list_of_urls)

    params = [(list_of_urls[i], to_dir) for i in range(len(list_of_urls))]
    pool = mp.Pool(processes)
    pool.starmap(download_file, params)
    pool.close()
    pool.join()