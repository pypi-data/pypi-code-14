"""
.. module:: hdf5
   :synopsis: Querying hdf5 files.

.. moduleauthor:: Danilo Horta <horta@ebi.ac.uk>


"""

import h5py
import numpy as np
import os
import tempfile
import shutil
import asciitree


def fetch(fp, path):
    """Fetches an array from hdf5 file.

    :param str fp: hdf5 file path.
    :param str path: path inside the hdf5 file.
    :returns: An :class:`numpy.ndarray` representation of the corresponding hdf5 dataset.
    """
    with h5py.File(fp, 'r') as f:
        return f[path][:]

def tree(f_or_filepath, root_name='/', ret=False, show_chunks=False):
    """Shows a human-friendly tree representation of the contents of
    a hdf5 file.

    :param f_or_filepath: hdf5 file path or a reference to an open one.
    :param str root_name: group to be the root of the tree.
    :param bool ret: Whether to return a string or print it.
    :param bool show_chunks: show the chunks.
    :returns str: String representation if is `ret=True`.
    """
    if isinstance(f_or_filepath, str):
        with h5py.File(f_or_filepath, 'r') as f:
            return _tree(f, root_name, ret, show_chunks)
    else:
        return _tree(f_or_filepath, root_name, ret, show_chunks)

def _findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

def _visititems(root, func, level=0, prefix=''):
    if root.name != '/':
        name = root.name
        eman = name[::-1]
        i1 = _findnth(eman, '/', level)
        name = '/' + eman[:i1][::-1]
        func(prefix + name, root)
    if not hasattr(root, 'keys'):
        return
    for k in root.keys():
        if root.file == root[k].file:
            _visititems(root[k], func, level+1, prefix)
        else:
            _visititems(root[k], func, 0, prefix + root.name)

def _tree(f, root_name='/', ret=False, show_chunks=False):
    _names = []
    def get_names(name, obj):
        if isinstance(obj, h5py.Dataset):
            dtype = str(obj.dtype)
            shape = str(obj.shape)
            if show_chunks:
                chunks = str(obj.chunks)
                _names.append("%s [%s, %s, %s]" % (name[1:], dtype, shape,
                                                   chunks))
            else:
                _names.append("%s [%s, %s]" % (name[1:], dtype, shape))
        else:
            _names.append(name[1:])

    # f._visititems(get_names)
    _visititems(f, get_names)
    class Node(object):
        def __init__(self, name, children):
            self.name = name
            self.children = children

        def __str__(self):
            return self.name
    root = Node(root_name, dict())

    def add_to_node(node, ns):
        if len(ns) == 0:
            return
        if ns[0] not in node.children:
            node.children[ns[0]] = Node(ns[0], dict())
        add_to_node(node.children[ns[0]], ns[1:])

    _names = sorted(_names)
    for n in _names:
        ns = n.split('/')
        add_to_node(root, ns)

    def child_iter(node):
        keys = node.children.keys()
        indices = np.argsort(keys)
        indices = np.asarray(indices)
        return list(np.asarray(node.children.values())[indices])

    msg = asciitree.draw_tree(root, child_iter)
    if ret:
        return msg
    print(msg)

def copy_memmap_h5dt(arr, dt):
    """Copies a :class:`numpy.memmap` to a hdf5 dataset."""
    if arr.ndim > 2:
        raise Exception("I don't know how to handle arrays" +
                        " with more than 2 dimensions yet.")
    assert arr.shape == dt.shape
    if arr.ndim == 1:
        dt[:] = arr[:]
    else:
        if dt.chunks is not None:
            chunk_row = dt.chunks[0]
        else:
            chunk_row = 512
        r = 0
        while r < arr.shape[0]:
            re = r + chunk_row
            re = min(re, arr.shape[0])
            dt[r:re,:] = arr[r:re,:]
            r = re

def _good_chunk(dataset):
    if hasattr(dataset, 'chunks'):
        return dataset.chunks
    c = 256
    ndim = len(dataset.shape)
    chunks = (min(c, dataset.shape[i]) for i in range(ndim))
    return chunks

def change_layout(fp, path, chunks, compression='gzip'):
    """Changes layout of a HDF5 dataset."""
    import dask.array as da

    def do(f):
        dataset = f[path]
        gpath = os.path.dirname('/' + path)
        g = f[gpath]

        d = da.from_array(dataset, chunks=_good_chunk(dataset))

        name = os.path.basename(dataset.name)
        tmp_name = name + '_tmp_cfm92askj3'
        if tmp_name in g:
            del g[tmp_name]
        tmp_d = g.create_dataset(tmp_name, shape=dataset.shape,
                             dtype=dataset.dtype, chunks=chunks,
                             compression=compression)
        da.store(d, tmp_d)

        del g[name]
        g[name] = g[tmp_name]
        del g[tmp_name]

    if isinstance(fp, str):
        with h5py.File(fp, 'r+') as f:
            do(f)
    else:
        do(fp)

def change_layout_greedy(fp, path, chunks, compression='lzf', shuffle=True):
    """Changes layout of a HDF5 dataset, in a greedy manner."""
    def do(f):
        dataset = f[path]
        gpath = os.path.dirname('/' + path)
        g = f[gpath]

        d = dataset.value

        name = os.path.basename(dataset.name)
        tmp_name = name + '_tmp_cfm92askj3'
        if tmp_name in g:
            del g[tmp_name]

        g.create_dataset(tmp_name, data=d, shape=dataset.shape,
                         dtype=dataset.dtype, chunks=chunks,
                         compression=compression, shuffle=shuffle)

        del g[name]
        g[name] = g[tmp_name]
        del g[tmp_name]

    if isinstance(fp, str):
        with h5py.File(fp, 'r+') as f:
            do(f)
    else:
        do(fp)

def convert_matrices_to_row_layout(f):
    """Changes layout of a HDF5 2-by-2 dataset into C-matrix layout."""
    def foo(path, node, f):
        if isinstance(node, h5py.Dataset) and len(node.shape) == 2:
            change_layout_greedy(f, path, chunks=(1, node.shape[1]))
    _visititems(f, lambda path, node: foo(path, node, f))

def convert_matrices_to_col_layout(f):
    """Changes layout of a HDF5 2-by-2 dataset into Fortran-matrix layout."""
    def foo(path, node, f):
        if isinstance(node, h5py.Dataset) and len(node.shape) == 2:
            change_layout_greedy(f, path, chunks=(node.shape[0], 1))
    _visititems(f, lambda path, node: foo(path, node, f))

def copy_h5dt_memmap_filepath(dt, fp):
    """Copies a HDF5 dataset to a `numpy.memmap`."""

    arr = np.memmap(fp, mode='w+', shape=dt.shape, dtype=dt.dtype)
    if arr.ndim > 2:
        raise Exception("I don't know how to handle arrays" +
                        " with more than 2 dimensions yet.")
    assert arr.shape == dt.shape

    if len(dt.shape) == 1:
        arr[:] = dt[:]
        del arr
    else:
        if dt.chunks is not None:
            chunk_row = dt.chunks[0]
        else:
            chunk_row = 512
        r = 0
        del arr
        while r < dt.shape[0]:
            arr = np.memmap(fp, mode='r+', shape=dt.shape, dtype=dt.dtype)
            re = r + chunk_row
            re = min(re, dt.shape[0])
            s = np.s_[r:re,:]
            dt.read_direct(arr, s, s)
            r = re
            del arr

class Memmap(object):
    """Represents a HDF5 dataset as a `numpy.memmap`."""
    def __init__(self, filepath, path, readonly=True, tmp_folder=None):
        self._filepath = filepath
        self._path = path
        self._folder = None
        self._X = None
        self._readonly = readonly
        self._tmp_folder = tmp_folder

    def __enter__(self):
        self._folder = tempfile.mkdtemp(dir=self._tmp_folder)
        with h5py.File(self._filepath, 'r', libversion='latest') as f:
            dt = f[self._path]
            shape = dt.shape
            dtype = dt.dtype
            copy_h5dt_memmap_filepath(dt, os.path.join(self._folder, 'X'))

        mode = 'r' if self._readonly else 'r+'
        X = np.memmap(os.path.join(self._folder, 'X'), mode=mode,
                      shape=shape, dtype=dtype)
        self._X = X
        return X
    def __exit__(self, *args):
        del self._X
        shutil.rmtree(self._folder)

class XBuffRows(object):
    """Interates over HDF5 dataset rows, buffering beforehand."""
    def __init__(self, X, row_indices, col_slice, buff_size=1000):
        buff_size = min(min(buff_size, X.shape[0]), len(row_indices))
        self._X = X
        self._row = 0
        self._row_buff = -1
        self._buff_size = buff_size
        self._row_indices = row_indices
        self._col_slice = col_slice
        ncols = len(np.empty(X.shape[1])[col_slice])
        self._Xbuff = np.empty((len(row_indices), ncols), dtype=X.dtype)
        self._arr_buff = np.empty(buff_size, dtype=X.dtype)

    def __iter__(self):
        return self

    def _extract_buffer(self, row_indices):
        cs = self._col_slice
        if isinstance(self._X, h5py.Dataset):
            srii = np.argsort(row_indices)
            sri = row_indices[srii]
            try:
                self._X.read_direct(self._Xbuff, np.s_[sri,cs], np.s_[srii,:])
            except TypeError:
                for (i, csi) in enumerate(cs):
                    self._X.read_direct(self._arr_buff, np.s_[sri,csi],
                                        np.s_[:])
                    self._Xbuff[np.s_[srii,i]] = self._arr_buff
        else:
            self._Xbuff[:len(row_indices),:] = self._X[row_indices,cs]

    def next(self):
        if self._row >= len(self._row_indices):
            raise StopIteration

        if self._row_buff == -1:
            l = self._row
            r = l + self._buff_size
            r = min(r, len(self._row_indices))
            self._extract_buffer(self._row_indices[l:r])
            self._row_buff = 0

        vec = self._Xbuff[self._row_buff,:]
        self._row_buff += 1
        if self._row_buff >= self._Xbuff.shape[0]:
            self._row_buff = -1
        self._row += 1

        return vec

def do_convert_layout(args):
    with h5py.File(args.filepath, 'r+') as f:
        if args.type == 'row':
            convert_matrices_to_row_layout(f)
        elif args.type == 'col':
            convert_matrices_to_col_layout(f)
        else:
            raise ValueError('Unknown layout type: %s.' % args.type)

def do_see(args):
    tree(args.filepath, show_chunks=args.show_chunks)

def entry_point():
    from argparse import ArgumentParser
    p = ArgumentParser()
    sub = p.add_subparsers()

    s = sub.add_parser('see')
    s.add_argument('filepath')
    s.add_argument('--show-chunks', dest='show_chunks', action='store_true')
    s.add_argument('--no-show-chunks', dest='show_chunks', action='store_false')
    s.set_defaults(func=do_see, show_chunks=False)

    s = sub.add_parser('convert-layout')
    s.add_argument('filepath')
    s.add_argument('type')
    s.set_defaults(func=do_convert_layout)

    args = p.parse_args()
    func = args.func
    del args.func
    func(args)
