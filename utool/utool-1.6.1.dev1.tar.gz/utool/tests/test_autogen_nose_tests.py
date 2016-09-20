from utool.util_class import *  # NOQA
from utool.util_progress import *  # NOQA
from utool.util_cache import *  # NOQA
from utool.util_list import *  # NOQA
from utool.util_inspect import *  # NOQA
from utool.util_dict import *  # NOQA
from utool.util_dev import *  # NOQA
from utool.util_time import *  # NOQA
from utool.util_type import *  # NOQA
from utool.util_csv import *  # NOQA
from utool.util_iter import *  # NOQA
from utool.util_tags import *  # NOQA
from utool.util_print import *  # NOQA
from utool.util_arg import *  # NOQA
from utool.util_graph import *  # NOQA
from utool.util_import import *  # NOQA
from utool.util_parallel import *  # NOQA
from utool.util_cplat import *  # NOQA
from utool.util_str import *  # NOQA
from utool.util_gridsearch import *  # NOQA
from utool.util_numpy import *  # NOQA
from utool.util_dbg import *  # NOQA
from utool.util_decor import *  # NOQA
from utool.util_grabdata import *  # NOQA
from utool.util_depricated import *  # NOQA
from utool.util_path import *  # NOQA
from utool.util_regex import *  # NOQA
from utool.util_tests import *  # NOQA
from utool.util_autogen import *  # NOQA
from utool.util_hash import *  # NOQA
from utool.util_alg import *  # NOQA
from utool.util_resources import *  # NOQA


def test_make_class_method_decorator_0():
    import utool as ut
    class CheeseShop(object):
        def __init__(self):
            import utool as ut
            ut.inject_all_external_modules(self)
    cheeseshop_method = ut.make_class_method_decorator(CheeseShop)
    shop1 = CheeseShop()
    assert not hasattr(shop1, 'has_cheese'), 'have not injected yet'
    @cheeseshop_method
    def has_cheese(self):
        return False
    shop2 = CheeseShop()
    assert shop2.has_cheese() is False, 'external method not injected'
    print('Cheese shop does not have cheese. All is well.')


def test_test_reloading_metaclass_0():
    result = test_reloading_metaclass()
    print(result)


def test_ProgChunks_0():
    import utool as ut
    list_ = range(100)
    chunksize = 10
    nInput = None
    progiter_ = ProgChunks(list_, chunksize, nInput)
    iter_ = iter(progiter_)
    chunk = six.next(iter_)
    assert len(chunk) == 10
    rest = ut.flatten(list(progiter_))
    assert len(rest) == 90


def test_ProgressIter_0():
    import utool as ut
    from six.moves import range
    num = 1000
    num2 = 10001
    results1 = [x for x in ut.ProgressIter(range(num), wfreq=10, adjust=True)]
    results4 = [x for x in ut.ProgressIter(range(num), wfreq=1, adjust=True)]
    results2 = [x for x in range(num)]
    results3 = [x for x in ut.progiter((y + 1 for y in range(num2)),
                                       nTotal=num2, wfreq=1000,
                                       backspace=True, adjust=True)]
    assert results1 == results2


def test_test_progress_0():
    test_progress()


def test_LRUDict_0():
    max_size = 5
    self = LRUDict(max_size)
    for count in range(0, 5):
        self[count] = count
    print(self)
    self[0]
    for count in range(5, 8):
        self[count] = count
    print(self)
    del self[5]
    assert 4 in self
    result = ('self = %r' % (self,))
    print(result)
    assert str(result) == u'self = LRUDict({\n    4: 4,\n    0: 0,\n    6: 6,\n    7: 7,\n})'


def test_LazyDict_0():
    import utool as ut
    self = ut.LazyDict()
    self['foo'] = lambda: 5
    self['bar'] = 4
    try:
        self['foo'] = lambda: 9
        assert False, 'should not be able to override computable functions'
    except ValueError:
        pass
    self['biz'] = lambda: 9
    d = {}
    d.update(**self)
    self['spam'] = lambda: 'eggs'
    self.printinfo()
    print(self.tostring(is_eager=False))


def test__args2_fpath_0():
    from utool.util_cache import _args2_fpath
    import utool as ut
    dpath = 'F:\\data\\work\\PZ_MTEST\\_ibsdb\\_ibeis_cache'
    fname = 'normalizer_'
    cfgstr = u'PZ_MTEST_DSUUIDS((9)67j%dr%&bl%4oh4+)_QSUUIDS((9)67j%dr%&bl%4oh4+)zebra_plains_vsone_NN(single,K1+1,last,cks1024)_FILT(ratio<0.625;1.0,fg;1.0)_SV(0.01;2;1.57minIn=4,nRR=50,nsum,)_AGG(nsum)_FLANN(4_kdtrees)_FEATWEIGHT(ON,uselabel,rf)_FEAT(hesaff+sift_)_CHIP(sz450)'
    ext = '.cPkl'
    write_hashtbl = False
    fpath = _args2_fpath(dpath, fname, cfgstr, ext, write_hashtbl)
    result = str(ut.ensure_unixslash(fpath))
    target = 'F:/data/work/PZ_MTEST/_ibsdb/_ibeis_cache/normalizer_xfylfboirymmcpfg.cPkl'
    ut.assert_eq(result, target)


def test_cached_func_0():
    import utool as ut
    def costly_func(a, b, c='d', *args, **kwargs):
        return ([a] * b, c, args, kwargs)
    ans0 = costly_func(41, 3)
    ans1 = costly_func(42, 3)
    closure_ = ut.cached_func('costly_func', appname='utool_test',
                              key_argx=[0, 1])
    efficient_func = closure_(costly_func)
    ans2 = efficient_func(42, 3)
    ans3 = efficient_func(42, 3)
    ans4 = efficient_func(41, 3)
    ans5 = efficient_func(41, 3)
    assert ans1 == ans2
    assert ans2 == ans3
    assert ans5 == ans4
    assert ans5 == ans0
    assert ans1 != ans0


def test_from_json_0():
    import utool as ut
    json_str = 'just a normal string'
    json_str = '["just a normal string"]'
    allow_pickle = False
    val = from_json(json_str, allow_pickle)
    result = ('val = %s' % (ut.repr2(val),))
    print(result)


def test_to_json_0():
    import utool as ut
    import numpy as np
    import uuid
    val = [
        '{"foo": "not a dict"}',
        1.3,
        [1],
        slice(1, None, 1),
        b'an ascii string',
        np.array([1, 2, 3]),
        ut.get_zero_uuid(),
        ut.LazyDict(x='fo'),
        ut.LazyDict,
    ]
    #val = ut.LazyDict(x='fo')
    allow_pickle = True
    if not allow_pickle:
        val = val[:-2]
    json_str = ut.to_json(val, allow_pickle=allow_pickle)
    result = ut.repr3(json_str)
    reload_val = ut.from_json(json_str, allow_pickle=allow_pickle)
    # Make sure pickle doesnt happen by default
    try:
        json_str = ut.to_json(val)
        assert False or not allow_pickle, 'expected a type error'
    except TypeError:
        print('Correctly got type error')
    try:
        json_str = ut.from_json(val)
        assert False, 'expected a type error'
    except TypeError:
        print('Correctly got type error')
    print(result)
    print('original = ' + ut.repr3(val, nl=1))
    print('reconstructed = ' + ut.repr3(reload_val, nl=1))
    assert reload_val[6] == val[6]
    assert reload_val[6] is not val[6]


def test_delete_items_by_index_0():
    list_ = [8, 1, 8, 1, 6, 6, 3, 4, 4, 5, 6]
    index_list = [2, -1]
    result = delete_items_by_index(list_, index_list)
    print(result)
    assert str(result) == u'[8, 1, 1, 6, 6, 3, 4, 4, 5]'


def test_depth_profile_0():
    list_ = [[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]]
    result = depth_profile(list_)
    print(result)
    assert str(result) == u'(2, 3, 4)'


def test_depth_profile_1():
    list_ = [[[[[1]]], [3, 4, 33]], [[1], [2, 3], [4, [5, 5]]], [1, 3]]
    result = depth_profile(list_)
    print(result)
    assert str(result) == u'[[(1, 1, 1), 3], [1, 2, [1, 2]], 2]'


def test_depth_profile_2():
    list_ = [[[[[1]]], [3, 4, 33]], [[1], [2, 3], [4, [5, 5]]], [1, 3]]
    result = depth_profile(list_, max_depth=1)
    print(result)
    assert str(result) == u"[[(1, '1'), 3], [1, 2, [1, '2']], 2]"


def test_depth_profile_3():
    list_ = [[[1, 2], [1, 2, 3]], None]
    result = depth_profile(list_, compress_homogenous=True)
    print(result)
    assert str(result) == u'[[2, 3], 1]'


def test_depth_profile_4():
    list_ = [[3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [9, 5, 3], [2, 2]]
    result = depth_profile(list_, compress_homogenous=True, compress_consecutive=True)
    print(result)
    assert str(result) == u'[2] * 6 + [3, 2]'


def test_depth_profile_5():
    list_ = [[[3, 9], 2], [[3, 9], 2], [[3, 9], 2], [[3, 9], 2]]  #, [3, 2], [3, 2]]
    result = depth_profile(list_, compress_homogenous=True, compress_consecutive=True)
    print(result)
    assert str(result) == u'(4, [2, 1])'


def test_depth_profile_6():
    list_ = [[[[1, 2]], [1, 2]], [[[1, 2]], [1, 2]], [[[0, 2]], [1]]]
    result1 = depth_profile(list_, compress_homogenous=True, compress_consecutive=False)
    result2 = depth_profile(list_, compress_homogenous=True, compress_consecutive=True)
    result = str(result1) + '\n' + str(result2)
    print(result)
    assert str(result) == u'[[(1, 2), 2], [(1, 2), 2], [(1, 2), 1]]\n[[(1, 2), 2]] * 2 + [[(1, 2), 1]]'


def test_depth_profile_7():
    list_ = [[{'a': [1, 2], 'b': [3, 4, 5]}, [1, 2, 3]], None]
    result = depth_profile(list_, compress_homogenous=True)
    print(result)


def test_depth_profile_8():
    list_ = [[[1]], [[[1, 1], [1, 1]]], [[[[1, 3], 1], [[1, 3, 3], 1, 1]]]]
    result = depth_profile(list_, compress_homogenous=True)
    print(result)


def test_depth_profile_9():
    list_ = []
    result = depth_profile(list_)
    print(result)


def test_depth_profile_10():
    fm1 = [[0, 0], [0, 0]]
    fm2 = [[0, 0], [0, 0], [0, 0]]
    fm3 = [[0, 0], [0, 0], [0, 0], [0, 0]]
    list_ = [0, 0, 0]
    list_ = [fm1, fm2, fm3]
    max_depth = 0
    new_depth = True
    result = depth_profile(list_, max_depth=max_depth, new_depth=new_depth)
    print(result)


def test_find_list_indexes_0():
    list_ = ['a', 'b', 'c']
    item_list = ['d', 'c', 'b', 'f']
    index_list = find_list_indexes(list_, item_list)
    result = ('index_list = %r' % (index_list,))
    print(result)
    assert str(result) == u'index_list = [None, 2, 1, None]'


def test_find_nonconsec_indices_0():
    import numpy as np
    unique_vals = np.array([-2, -1,  1,  2, 10])
    max_ = unique_vals.max()
    min_ = unique_vals.min()
    range_ = max_ - min_
    consec_vals = np.linspace(min_, max_ + 1, range_ + 2)
    missing_ixs = find_nonconsec_indices(unique_vals, consec_vals)
    result = (consec_vals[missing_ixs])
    assert str(result) == u'[ 0.  3.  4.  5.  6.  7.  8.  9.]'


def test_flatten_0():
    import utool as ut
    list_ = [['a', 'b'], ['c', 'd']]
    unflat_list2 = flatten(list_)
    result = ut.list_str(unflat_list2, nl=False)
    print(result)
    assert str(result) == u"['a', 'b', 'c', 'd']"


def test_index_to_boolmask_0():
    import utool as ut
    index_list = [0, 1, 4]
    maxval = 5
    mask = ut.index_to_boolmask(index_list, maxval)
    result = ('mask = %s' % (ut.repr2(mask, nl=0)))
    print(result)
    assert str(result) == u'mask = [True, True, False, False, True]'


def test_invertible_flatten_0():
    import utool as ut
    unflat_list = [[1, 2, 3], [4, 5], [6, 6]]
    flat_list, reverse_list = invertible_flatten(unflat_list)
    result = ('flat_list = %s\n' % (ut.repr2(flat_list),))
    result += ('reverse_list = %s' % (ut.repr2(reverse_list),))
    print(result)
    assert str(result) == u'flat_list = [1, 2, 3, 4, 5, 6, 6]\nreverse_list = [[0, 1, 2], [3, 4], [5, 6]]'


def test_invertible_flatten2_0():
    import utool
    utool.util_list
    unflat_list = [[5], [2, 3, 12, 3, 3], [9], [13, 3], [5]]
    flat_list, cumlen_list = invertible_flatten2(unflat_list)
    unflat_list2 = unflatten2(flat_list, cumlen_list)
    assert unflat_list2 == unflat_list
    result = ((flat_list, cumlen_list))
    print(result)
    assert str(result) == u'([5, 2, 3, 12, 3, 3, 9, 13, 3, 5], [1, 6, 7, 9, 10])'


def test_is_subset_of_any_0():
    # build test data
    set_ = {1, 2}
    other_sets = [{1, 4}, {3, 2, 1}]
    # execute function
    result = is_subset_of_any(set_, other_sets)
    # verify results
    print(result)
    assert str(result) == u'True'


def test_is_subset_of_any_1():
    # build test data
    set_ = {1, 2}
    other_sets = [{1, 4}, {3, 2}]
    # execute function
    result = is_subset_of_any(set_, other_sets)
    # verify results
    print(result)
    assert str(result) == u'False'


def test_list_argmaxima_0():
    list_ = np.array([1, 2, 3, 3, 3, 2, 1])
    argmaxima = list_argmaxima(list_)
    result = ('argmaxima = %s' % (str(argmaxima),))
    print(result)
    assert str(result) == u'argmaxima = [2 3 4]'


def test_list_depth_0():
    list_ = [[[[[1]]], [3]], [[1], [3]], [[1], [3]]]
    result = (list_depth(list_, _depth=0))
    print(result)


def test_list_inverse_take_0():
    import utool as ut
    # build test data
    rank_list = [3, 2, 4, 1, 9, 2]
    prop_list = [0, 1, 2, 3, 4, 5]
    index_list = ut.argsort(rank_list)
    sorted_prop_list = ut.take(prop_list, index_list)
    # execute function
    list_ = sorted_prop_list
    output_list_  = list_inverse_take(list_, index_list)
    output_list2_ = ut.take(list_, ut.argsort(index_list))
    assert output_list_ == prop_list
    assert output_list2_ == prop_list
    # verify results
    result = str(output_list_)
    print(result)


def test_list_reshape_0():
    import utool as ut
    import numpy as np
    list_ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    new_shape = (2, 2, 3)
    newlist = list_reshape(list_, new_shape)
    depth = ut.depth_profile(newlist)
    result = ('list_ = %s' % (ut.repr2(newlist, nl=1),))
    print('depth = %r' % (depth,))
    print(result)
    newlist2 = np.reshape(list_, depth).tolist()
    ut.assert_eq(newlist, newlist2)


def test_list_roll_0():
    list_ = [1, 2, 3, 4, 5]
    n = 2
    result = list_roll(list_, n)
    print(result)
    assert str(result) == u'[4, 5, 1, 2, 3]'


def test_list_transpose_0():
    list_ = [[1, 2], [3, 4]]
    result = list_transpose(list_)
    print(result)
    assert str(result) == u'[(1, 3), (2, 4)]'


def test_list_transpose_1():
    list_ = []
    result = list_transpose(list_, shape=(0, 5))
    print(result)
    assert str(result) == u'[[], [], [], [], []]'


def test_list_transpose_2():
    list_ = [[], [], [], [], []]
    result = list_transpose(list_)
    print(result)
    assert str(result) == u'[]'


def test_list_transpose_3():
    import utool as ut
    list_ = [[1, 2, 3], [3, 4]]
    ut.assert_raises(ValueError, list_transpose, list_)


def test_list_type_profile_0():
    import numpy as np
    sequence = [[1, 2], np.array([1, 2, 3], dtype=np.int32), (np.array([1, 2, 3], dtype=np.int32),)]
    compress_homogenous = True
    level_type_str = list_type_profile(sequence, compress_homogenous)
    result = ('level_type_str = %s' % (str(level_type_str),))
    print(result)
    assert str(result) == u'level_type_str = list(list(int*2), ndarray[int32], tuple(ndarray[int32]*1))'


def test_listclip_0():
    import utool as ut
    # build test data
    list_ = [1, 2, 3, 4, 5]
    result_list = []
    # execute function
    num = 3
    result_list += [ut.listclip(list_, num)]
    num = 9
    result_list += [ut.listclip(list_, num)]
    # verify results
    result = ut.list_str(result_list)
    print(result)
    assert str(result) == u'[\n    [1, 2, 3],\n    [1, 2, 3, 4, 5],\n]'


def test_listclip_1():
    import utool as ut
    # build test data
    list_ = [1, 2, 3, 4, 5]
    result_list = []
    # execute function
    num = 3
    result = ut.listclip(list_, num, fromback=True)
    print(result)
    assert str(result) == u'[3, 4, 5]'


def test_listfind_0():
    list_ = ['a', 'b', 'c']
    tofind = 'b'
    result = listfind(list_, tofind)
    print(result)
    assert str(result) == u'1'


def test_make_index_lookup_0():
    import utool as ut
    list_ = [5, 3, 8, 2]
    idx2_item = ut.make_index_lookup(list_)
    result = ut.dict_str(idx2_item, nl=False)
    assert ut.dict_take(idx2_item, list_) == list(range(len(list_)))
    print(result)
    assert str(result) == u'{2: 3, 3: 1, 5: 0, 8: 2}'


def test_priority_argsort_0():
    import utool as ut
    list_ = [2, 4, 6, 8, 10]
    priority = [8, 2, 6, 9]
    sortx = priority_argsort(list_, priority)
    reordered_list = priority_sort(list_, priority)
    assert ut.take(list_, sortx) == reordered_list
    result = str(sortx)
    print(result)
    assert str(result) == u'[3, 0, 2, 1, 4]'


def test_priority_sort_0():
    list_ = [2, 4, 6, 8, 10]
    priority = [8, 2, 6, 9]
    reordered_list = priority_sort(list_, priority)
    result = str(reordered_list)
    print(result)
    assert str(result) == u'[8, 2, 6, 4, 10]'


def test_replace_nones_0():
    # build test data
    list_ = [None, 0, 1, 2]
    repl = -1
    # execute function
    repl_list = replace_nones(list_, repl)
    # verify results
    result = str(repl_list)
    print(result)
    assert str(result) == u'[-1, 0, 1, 2]'


def test_search_list_0():
    import utool as ut
    text_list = ['ham', 'jam', 'eggs', 'spam']
    pattern = '.am'
    flags = 0
    (valid_index_list, valid_match_list) = ut.search_list(text_list, pattern, flags)
    result = str(valid_index_list)
    print(result)
    assert str(result) == u'[0, 1, 3]'


def test_setdiff_0():
    import utool as ut
    list1 = ['featweight_rowid', 'feature_rowid', 'config_rowid', 'featweight_forground_weight']
    list2 = [u'featweight_rowid']
    new_list = setdiff_ordered(list1, list2)
    result = ut.list_str(new_list, nl=False)
    print(result)
    assert str(result) == u"['feature_rowid', 'config_rowid', 'featweight_forground_weight']"


def test_setintersect_ordered_0():
    list1 = [1, 2, 3, 5, 8, 13, 21]
    list2 = [6, 4, 2, 21, 8]
    new_list = setintersect_ordered(list1, list2)
    result = new_list
    print(result)
    assert str(result) == u'[2, 8, 21]'


def test_sortedby_0():
    import utool
    list_    = [1, 2, 3, 4, 5]
    key_list = [2, 5, 3, 1, 5]
    result = utool.sortedby(list_, key_list, reverse=True)
    assert str(result) == u'[5, 2, 3, 1, 4]'


def test_sortedby2_0():
    import utool as ut
    item_list = [1, 2, 3, 4, 5]
    key_list1 = [1, 1, 2, 3, 4]
    key_list2 = [2, 1, 4, 1, 1]
    args = (key_list1, key_list2)
    kwargs = dict(reverse=False)
    result = ut.sortedby2(item_list, *args, **kwargs)
    print(result)
    assert str(result) == u'[2, 1, 3, 4, 5]'


def test_sortedby2_1():
    # Python 3 Compatibility Test
    import utool as ut
    item_list = [1, 2, 3, 4, 5]
    key_list1 = ['a', 'a', 2, 3, 4]
    key_list2 = ['b', 'a', 4, 1, 1]
    args = (key_list1, key_list2)
    kwargs = dict(reverse=False)
    result = ut.sortedby2(item_list, *args, **kwargs)
    print(result)
    assert str(result) == u'[3, 4, 5, 2, 1]'


def test_take_0():
    list_ = [0, 1, 2, 3]
    index_list = [2, 0]
    result = take(list_, index_list)
    print(result)
    assert str(result) == u'[2, 0]'


def test_take_1():
    list_ = [0, 1, 2, 3]
    index = 2
    result = take(list_, index)
    print(result)
    assert str(result) == u'2'


def test_take_2():
    list_ = [0, 1, 2, 3]
    index = slice(1, None, 2)
    result = take(list_, index)
    print(result)
    assert str(result) == u'[1, 3]'


def test_take_column_0():
    list_ = [['a', 'b'], ['c', 'd']]
    colx = 0
    result = take_column(list_, colx)
    import utool as ut
    result = ut.list_str(result, nl=False)
    print(result)
    assert str(result) == u"['a', 'c']"


def test_take_column_1():
    list_ = [['a', 'b'], ['c', 'd']]
    colx = [1, 0]
    result = take_column(list_, colx)
    import utool as ut
    result = ut.list_str(result, nl=False)
    print(result)
    assert str(result) == u"[['b', 'a'], ['d', 'c']]"


def test_take_column_2():
    list_ = [{'spam': 'EGGS', 'ham': 'SPAM'}, {'spam': 'JAM', 'ham': 'PRAM'}]
    # colx can be a key or list of keys as well
    colx = ['spam']
    result = take_column(list_, colx)
    import utool as ut
    result = ut.list_str(result, nl=False)
    print(result)
    assert str(result) == u"[['EGGS'], ['JAM']]"


def test_unflat_map_0():
    vectorized = False
    kwargs = {}
    def func(x):
        return x + 1
    unflat_items = [[], [1, 2, 3], [4, 5], [6, 7, 8, 9], [], []]
    unflat_vals = unflat_map(func, unflat_items)
    result = str(unflat_vals)
    print(result)
    assert str(result) == u'[[], [2, 3, 4], [5, 6], [7, 8, 9, 10], [], []]'


def test_unflat_unique_rowid_map_0():
    import utool as ut
    kwargs = {}
    unflat_rowids = [[1, 2, 3], [2, 5], [1], []]
    num_calls0 = [0]
    num_input0 = [0]
    def func0(rowids, num_calls0=num_calls0, num_input0=num_input0):
        num_calls0[0] += 1
        num_input0[0] += len(rowids)
        return [rowid + 10 for rowid in rowids]
    func = func0
    unflat_vals = unflat_unique_rowid_map(func, unflat_rowids, **kwargs)
    result = [arr.tolist() for arr in unflat_vals]
    print(result)
    ut.assert_eq(num_calls0[0], 1)
    ut.assert_eq(num_input0[0], 4)
    assert str(result) == u'[[11, 12, 13], [12, 15], [11], []]'


def test_unflat_unique_rowid_map_1():
    import utool as ut
    import numpy as np
    kwargs = {}
    unflat_rowids = [[1, 2, 3], [2, 5], [1], []]
    num_calls1 = [0]
    num_input1 = [0]
    def func1(rowids, num_calls1=num_calls1, num_input1=num_input1, np=np):
        num_calls1[0] += 1
        num_input1[0] += len(rowids)
        return [np.array([rowid + 10, rowid, 3]) for rowid in rowids]
    func = func1
    unflat_vals = unflat_unique_rowid_map(func, unflat_rowids, **kwargs)
    result = [arr.tolist() for arr in unflat_vals]
    print(result)
    ut.assert_eq(num_calls1[0], 1)
    ut.assert_eq(num_input1[0], 4)
    assert str(result) == u'[[[11, 1, 3], [12, 2, 3], [13, 3, 3]], [[12, 2, 3], [15, 5, 3]], [[11, 1, 3]], []]'


def test_unflatten2_0():
    import utool
    utool.util_list
    flat_list = [5, 2, 3, 12, 3, 3, 9, 13, 3, 5]
    cumlen_list = [ 1,  6,  7,  9, 10]
    unflat_list2 = unflatten2(flat_list, cumlen_list)
    result = (unflat_list2)
    print(result)
    assert str(result) == u'[[5], [2, 3, 12, 3, 3], [9], [13, 3], [5]]'


def test_unique_ordered_0():
    list_ = [4, 6, 6, 0, 6, 1, 0, 2, 2, 1]
    unique_list = unique_ordered(list_)
    result = ('unique_list = %s' % (str(unique_list),))
    print(result)
    assert str(result) == u'unique_list = [4, 6, 0, 1, 2]'


def test_xor_lists_0():
    args = ([True, False, False, True], [True, True, False, False])
    result = xor_lists(*args)
    print(result)
    assert str(result) == u'[False, True, False, True]'


def test_argparse_funckw_0():
    import utool as ut
    func = get_instance_attrnames
    funckw = argparse_funckw(func)
    result = ('funckw = %s' % (ut.repr3(funckw),))
    print(result)
    assert str(result) == u"funckw = {\n    'default': True,\n    'with_methods': 'default',\n    'with_properties': 'default',\n}"


def test_find_child_kwarg_funcs_0():
    import utool as ut
    sourcecode = ut.codeblock(
        '''
        warped_patch1_list, warped_patch2_list = list(zip(*ut.ichunks(data, 2)))
        interact_patches(labels, warped_patch1_list, warped_patch2_list, flat_metadata, **kwargs)
        import sys
        sys.badcall(**kwargs)
        def foo():
            bar(**kwargs)
            ut.holymoly(**kwargs)
            baz()
            def biz(**kwargs):
                foo2(**kwargs)
        ''')
    child_funcnamess = ut.find_child_kwarg_funcs(sourcecode)
    print('child_funcnamess = %r' % (child_funcnamess,))
    assert 'foo2' not in child_funcnamess, 'foo2 should not be found'
    assert 'bar' in child_funcnamess, 'bar should be found'


def test_find_pyfunc_above_row_0():
    import utool as ut
    func = find_pyfunc_above_row
    fpath = meta_util_six.get_funcglobals(func)['__file__'].replace('.pyc', '.py')
    line_list = ut.read_from(fpath, aslines=True)
    row = meta_util_six.get_funccode(func).co_firstlineno + 1
    pyfunc, searchline = find_pyfunc_above_row(line_list, row)
    result = pyfunc
    print(result)
    assert str(result) == u'find_pyfunc_above_row'


def test_get_kwdefaults_0():
    import utool as ut
    func = dummy_func
    parse_source = True
    kwdefaults = get_kwdefaults(func, parse_source)
    print('kwdefaults = %s' % (ut.dict_str(kwdefaults),))


def test_help_members_0():
    import utool as ut
    obj = ut.DynStruct
    result = help_members(obj)
    print(result)


def test_infer_arg_types_and_descriptions_0():
    import utool
    argname_list = ['ibs', 'qaid', 'fdKfds', 'qfx2_foo']
    defaults = None
    tup = utool.infer_arg_types_and_descriptions(argname_list, defaults)
    argtype_list, argdesc_list, argdefault_list, hasdefault_list = tup


def test_infer_function_info_0():
    import utool as ut
    func = ut.infer_function_info
    #func = ut.Timer.tic
    func = ut.make_default_docstr
    funcinfo = infer_function_info(func)
    result = ut.dict_str(funcinfo.__dict__)
    print(result)


def test_iter_module_doctestable_0():
    import utool as ut
    modname = ut.get_argval('--modname', type_=str, default=None)
    kwargs = ut.argparse_funckw(iter_module_doctestable)
    module = ut.util_tests if modname is None else ut.import_modname(modname)
    debug_key = ut.get_argval('--debugkey', type_=str, default=None)
    kwargs['debug_key'] = debug_key
    doctestable_list = list(iter_module_doctestable(module, **kwargs))
    func_names = sorted(ut.get_list_column(doctestable_list, 0))
    print(ut.list_str(func_names))


def test_parse_kwarg_keys_0():
    import utool as ut
    source = ("\n kwargs.get('foo', None)\n kwargs.pop('bar', 3)"
              "\n kwargs.pop('str', '3fd')\n kwargs.pop('str', '3f\'d')"
              "\n \"kwargs.get('baz', None)\"\n kwargs['foo2']")
    print(source)
    ut.exec_funckw(parse_kwarg_keys, globals())
    with_vals = True
    kwarg_keys = parse_kwarg_keys(source, with_vals=with_vals)
    result = ('kwarg_keys = %s' % (ut.repr2(kwarg_keys, nl=1),))
    assert 'baz' not in ut.take_column(kwarg_keys, 0)
    assert 'foo' in ut.take_column(kwarg_keys, 0)
    print(result)
    assert str(result) == u'kwarg_keys = [\n    (\'foo\', None),\n    (\'bar\', 3),\n    (\'str\', "\'3fd\'"),\n    (\'str\', "\'3f\'d\'"),\n    (\'foo2\', None),\n]'


def test_parse_return_type_0():
    import utool as ut
    sourcecode = ut.codeblock(
        'def foo(tmp=False):\n'
        '    bar = True\n'
        '    return bar\n'
    )
    returninfo = parse_return_type(sourcecode)
    result = ut.repr2(returninfo)
    print(result)
    assert str(result) == u"('?', 'bar', 'Returns', '')"


def test_parse_return_type_1():
    import utool as ut
    sourcecode = ut.codeblock(
        'def foo(tmp=False):\n'
        '    return True\n'
    )
    returninfo = parse_return_type(sourcecode)
    result = ut.repr2(returninfo)
    print(result)
    assert str(result) == u"('bool', 'True', 'Returns', '')"


def test_parse_return_type_2():
    import utool as ut
    sourcecode = ut.codeblock(
        'def foo(tmp=False):\n'
        '    for i in range(2): \n'
        '        yield i\n'
    )
    returninfo = parse_return_type(sourcecode)
    result = ut.repr2(returninfo)
    print(result)
    assert str(result) == u"('?', 'i', 'Yields', '')"


def test_parse_return_type_3():
    import utool as ut
    sourcecode = ut.codeblock(
        'def foo(tmp=False):\n'
        '    if tmp is True:\n'
        '        return (True, False)\n'
        '    elif tmp is False:\n'
        '        return 1\n'
        '    else:\n'
        '        bar = baz()\n'
        '        return bar\n'
    )
    returninfo = parse_return_type(sourcecode)
    result = ut.repr2(returninfo)
    print(result)
    assert str(result) == u"('tuple', '(True, False)', 'Returns', '')"


def test_recursive_parse_kwargs_0():
    import utool as ut
    root_func = iter_module_doctestable
    path_ = None
    result = ut.repr2(recursive_parse_kwargs(root_func), nl=1)
    print(result)
    assert str(result) == u"[\n    ('include_funcs', True),\n    ('include_classes', True),\n    ('include_methods', True),\n    ('include_builtin', True),\n    ('include_inherited', False),\n    ('debug_key', None),\n]"


def test_AutoVivification_0():
    dict_ = AutoVivification()
    # Notice that there is no KeyError
    dict_[0][10][100] = None
    result = ('dict_ = %r' % (dict_,))
    print(result)
    assert str(result) == u'dict_ = {0: {10: {100: None}}}'


def test_all_dict_combinations_0():
    import utool as ut
    varied_dict = {'logdist_weight': [0.0, 1.0], 'pipeline_root': ['vsmany'], 'sv_on': [True, False, None]}
    dict_list = all_dict_combinations(varied_dict)
    result = str(ut.list_str(dict_list))
    print(result)
    assert str(result) == u"[\n    {'logdist_weight': 0.0, 'pipeline_root': 'vsmany', 'sv_on': True},\n    {'logdist_weight': 0.0, 'pipeline_root': 'vsmany', 'sv_on': False},\n    {'logdist_weight': 0.0, 'pipeline_root': 'vsmany', 'sv_on': None},\n    {'logdist_weight': 1.0, 'pipeline_root': 'vsmany', 'sv_on': True},\n    {'logdist_weight': 1.0, 'pipeline_root': 'vsmany', 'sv_on': False},\n    {'logdist_weight': 1.0, 'pipeline_root': 'vsmany', 'sv_on': None},\n]"


def test_all_dict_combinations_lbls_0():
    import utool
    varied_dict = {'logdist_weight': [0.0, 1.0], 'pipeline_root': ['vsmany'], 'sv_on': [True, False, None]}
    comb_lbls = utool.all_dict_combinations_lbls(varied_dict)
    result = (utool.list_str(comb_lbls))
    print(result)
    assert str(result) == u"[\n    'logdist_weight=0.0,sv_on=True',\n    'logdist_weight=0.0,sv_on=False',\n    'logdist_weight=0.0,sv_on=None',\n    'logdist_weight=1.0,sv_on=True',\n    'logdist_weight=1.0,sv_on=False',\n    'logdist_weight=1.0,sv_on=None',\n]"


def test_all_dict_combinations_lbls_1():
    import utool as ut
    varied_dict = {'logdist_weight': [0.0], 'pipeline_root': ['vsmany'], 'sv_on': [True]}
    allow_lone_singles = True
    comb_lbls = ut.all_dict_combinations_lbls(varied_dict, allow_lone_singles=allow_lone_singles)
    result = (ut.list_str(comb_lbls))
    print(result)
    assert str(result) == u"[\n    'logdist_weight=0.0,pipeline_root=vsmany,sv_on=True',\n]"


def test_delete_dict_keys_0():
    import utool as ut
    # build test data
    dict_ = {'bread': 1, 'churches': 1, 'cider': 2, 'very small rocks': 2}
    key_list = ['duck', 'bread', 'cider']
    # execute function
    delete_dict_keys(dict_, key_list)
    # verify results
    result = ut.dict_str(dict_, nl=False)
    print(result)
    assert str(result) == u"{'churches': 1, 'very small rocks': 2}"


def test_dict_intersection_0():
    import utool as ut
    dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    dict2 = {'b': 2, 'c': 3, 'd': 5, 'e': 21, 'f': 42}
    combine = False
    mergedict_ = dict_intersection(dict1, dict2, combine)
    result = ('mergedict_ = %s' % (ut.dict_str(mergedict_, nl=False),))
    print(result)
    assert str(result) == u"mergedict_ = {'b': 2, 'c': 3}"


def test_dict_stack_0():
    import utool as ut
    dict1_ = {'a': 1, 'b': 2}
    dict2_ = {'a': 2, 'b': 3, 'c': 4}
    dict_stacked = dict_stack([dict1_, dict2_])
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [1, 2], 'b': [2, 3], 'c': [4]}"


def test_dict_stack_1():
    import utool as ut
    # Get equivalent behavior with dict_stack2?
    # Almost, as long as None is not part of the list
    dict1_ = {'a': 1, 'b': 2}
    dict2_ = {'a': 2, 'b': 3, 'c': 4}
    dict_stacked_ = dict_stack2([dict1_, dict2_])
    dict_stacked = {key: ut.filter_Nones(val) for key, val in dict_stacked_.items()}
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [1, 2], 'b': [2, 3], 'c': [4]}"


def test_dict_stack2_0():
    import utool as ut
    # Usual case: multiple dicts as input
    dict1_ = {'a': 1, 'b': 2}
    dict2_ = {'a': 2, 'b': 3, 'c': 4}
    dict_list = [dict1_, dict2_]
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [1, 2], 'b': [2, 3], 'c': [None, 4]}"


def test_dict_stack2_1():
    import utool as ut
    # Corner case: one dict as input
    dict1_ = {'a': 1, 'b': 2}
    dict_list = [dict1_]
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [1], 'b': [2]}"


def test_dict_stack2_2():
    import utool as ut
    # Corner case: zero dicts as input
    dict_list = []
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u'{}'


def test_dict_stack2_3():
    import utool as ut
    # Corner case: empty dicts as input
    dict_list = [{}]
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u'{}'


def test_dict_stack2_4():
    import utool as ut
    # Corner case: one dict is empty
    dict1_ = {'a': [1, 2], 'b': [2, 3]}
    dict2_ = {}
    dict_list = [dict1_, dict2_]
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [[1, 2], None], 'b': [[2, 3], None]}"


def test_dict_stack2_5():
    import utool as ut
    # Corner case: disjoint dicts
    dict1_ = {'a': [1, 2], 'b': [2, 3]}
    dict2_ = {'c': 4}
    dict_list = [dict1_, dict2_]
    dict_stacked = dict_stack2(dict_list)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [[1, 2], None], 'b': [[2, 3], None], 'c': [None, 4]}"


def test_dict_stack2_6():
    import utool as ut
    # Corner case: 3 dicts
    import utool as ut
    dict_list = [{'a': 1}, {'b': 1}, {'c': 1}, {'b': 2}]
    default = None
    dict_stacked = dict_stack2(dict_list, default=default)
    result = ut.repr2(dict_stacked, sorted_=True)
    print(result)
    assert str(result) == u"{'a': [1, None, None, None], 'b': [None, 1, None, 2], 'c': [None, None, 1, None]}"


def test_dict_subset_0():
    import utool as ut
    dict_ = {'K': 3, 'dcvs_clip_max': 0.2, 'p': 0.1}
    keys = ['K', 'dcvs_clip_max']
    d = tuple([])
    subdict_ = dict_subset(dict_, keys)
    result = ut.dict_str(subdict_, sorted_=True, newlines=False)
    print(result)
    assert str(result) == u"{'K': 3, 'dcvs_clip_max': 0.2}"


def test_dict_take_gen_0():
    import utool as ut
    dict_ = {1: 'a', 2: 'b', 3: 'c'}
    keys = [1, 2, 3, 4, 5]
    result = list(dict_take_gen(dict_, keys, None))
    result = ut.list_str(result, nl=False)
    print(result)
    assert str(result) == u"['a', 'b', 'c', None, None]"


def test_dict_take_gen_1():
    dict_ = {1: 'a', 2: 'b', 3: 'c'}
    keys = [1, 2, 3, 4, 5]
    try:
        print(list(dict_take_gen(dict_, keys)))
        result = 'did not get key error'
    except KeyError:
        result = 'correctly got key error'
    print(result)


def test_dict_take_pop_0():
    import utool as ut
    dict_ = {1: 'a', 'other': None, 'another': 'foo', 2: 'b', 3: 'c'}
    keys = [1, 2, 3, 4, 5]
    print('before: ' + ut.dict_str(dict_))
    result = list(dict_take_pop(dict_, keys, None))
    result = ut.list_str(result, nl=False)
    print('after: ' + ut.dict_str(dict_))
    assert len(dict_) == 2
    print(result)
    assert str(result) == u"['a', 'b', 'c', None, None]"


def test_dict_take_pop_1():
    import utool as ut
    dict_ = {1: 'a', 2: 'b', 3: 'c'}
    keys = [1, 2, 3, 4, 5]
    print('before: ' + ut.dict_str(dict_))
    try:
        print(list(dict_take_pop(dict_, keys)))
        result = 'did not get key error'
    except KeyError:
        result = 'correctly got key error'
    assert len(dict_) == 0
    print('after: ' + ut.dict_str(dict_))
    print(result)


def test_dict_union3_0():
    import utool as ut
    dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    dict2 = {'b': 2, 'c': 3, 'd': 5, 'e': 21, 'f': 42}
    combine_op = operator.add
    mergedict_ = dict_union3(dict1, dict2, combine_op)
    result = ('mergedict_ = %s' % (ut.dict_str(mergedict_, nl=False),))
    print(result)
    assert str(result) == u"mergedict_ = {'a': 1, 'b': 4, 'c': 6, 'd': 9, 'e': 21, 'f': 42}"


def test_flatten_dict_items_0():
    import utool as ut
    item_list     = [1, 2, 3, 4]
    groupids_list = [[1, 1, 1, 2], [1, 2, 2, 2], [1, 3, 1, 1]]
    dict_ = hierarchical_group_items(item_list, groupids_list)
    flatter_dict = flatten_dict_items(dict_)
    result = ('flatter_dict = ' + ut.dict_str(flatter_dict, nl=1))
    print(result)
    assert str(result) == u'flatter_dict = {\n    (1, 1, 1): [1],\n    (1, 2, 1): [3],\n    (1, 2, 3): [2],\n    (2, 2, 1): [4],\n}'


def test_get_dict_hashid_0():
    dict_ = {}
    dict_ = {'a': 'b'}
    dict_ = {'a': {'c': 'd'}}
    #dict_ = {'a': {'c': 'd'}, 1: 143, dict: set}
    dict_ = {'a': {'c': 'd'}, 1: 143 }
    hashid = get_dict_hashid(dict_)
    result = str(hashid)
    print(result)
    assert str(result) == u'oegknoalkrkojumi'


def test_group_items_0():
    import utool as ut
    item_list    = [ 'ham',      'jam',    'spam',     'eggs', 'cheese', 'bannana']
    groupid_list = ['protein', 'fruit', 'protein',  'protein',  'dairy',   'fruit']
    groupid2_items = ut.group_items(item_list, iter(groupid_list))
    result = ut.dict_str(groupid2_items, nl=False, strvals=False)
    print(result)
    assert str(result) == u"{'dairy': ['cheese'], 'fruit': ['jam', 'bannana'], 'protein': ['ham', 'spam', 'eggs']}"


def test_hierarchical_group_items_0():
    import utool as ut
    item_list     = [1, 2, 3, 4]
    groupids_list = [[1, 1, 2, 2]]
    tree = hierarchical_group_items(item_list, groupids_list)
    result = ('tree = ' + ut.dict_str(tree, nl=len(groupids_list) - 1))
    print(result)
    assert str(result) == u'tree = {1: [1, 2], 2: [3, 4]}'


def test_hierarchical_group_items_1():
    import utool as ut
    item_list     = [1, 2, 3, 4, 5, 6, 7, 8]
    groupids_list = [[1, 2, 1, 2, 1, 2, 1, 2], [3, 2, 2, 2, 3, 1, 1, 1]]
    tree = hierarchical_group_items(item_list, groupids_list)
    result = ('tree = ' + ut.dict_str(tree, nl=len(groupids_list) - 1))
    print(result)
    assert str(result) == u'tree = {\n    1: {1: [7], 2: [3], 3: [1, 5]},\n    2: {1: [6, 8], 2: [2, 4]},\n}'


def test_hierarchical_group_items_2():
    import utool as ut
    item_list     = [1, 2, 3, 4]
    groupids_list = [[1, 1, 1, 2], [1, 2, 2, 2], [1, 3, 1, 1]]
    tree = hierarchical_group_items(item_list, groupids_list)
    result = ('tree = ' + ut.dict_str(tree, nl=len(groupids_list) - 1))
    print(result)
    assert str(result) == u'tree = {\n    1: {\n        1: {1: [1]},\n        2: {1: [3], 3: [2]},\n    },\n    2: {\n        2: {1: [4]},\n    },\n}'


def test_hierarchical_map_vals_0():
    import utool as ut
    item_list     = [1, 2, 3, 4, 5, 6, 7, 8]
    groupids_list = [[1, 2, 1, 2, 1, 2, 1, 2], [3, 2, 2, 2, 3, 1, 1, 1]]
    tree = ut.hierarchical_group_items(item_list, groupids_list)
    len_tree = ut.hierarchical_map_vals(len, tree)
    result = ('len_tree = ' + ut.dict_str(len_tree, nl=1))
    print(result)
    assert str(result) == u'len_tree = {\n    1: {1: 1, 2: 1, 3: 2},\n    2: {1: 2, 2: 2},\n}'


def test_invert_dict_0():
    import utool as ut
    dict_ = {'a': 1, 'b': 2}
    inverted_dict = invert_dict(dict_)
    result = ut.dict_str(inverted_dict, nl=False)
    print(result)
    assert str(result) == u"{1: 'a', 2: 'b'}"


def test_invert_dict_1():
    import utool as ut
    dict_ = OrderedDict([(2, 'good',), (1, 'ok',), (0, 'junk',), (None, 'UNKNOWN',)])
    inverted_dict = invert_dict(dict_)
    result = ut.dict_str(inverted_dict, nl=False)
    print(result)
    assert str(result) == u"{'good': 2, 'ok': 1, 'junk': 0, 'UNKNOWN': None}"


def test_invert_dict_2():
    import utool as ut
    dict_ = {'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 2}
    inverted_dict = invert_dict(dict_, unique_vals=False)
    inverted_dict = ut.map_dict_vals(sorted, inverted_dict)
    result = ut.dict_str(inverted_dict, nl=False)
    print(result)
    assert str(result) == u"{0: ['b', 'c', 'd', 'e'], 1: ['a'], 2: ['f']}"


def test_merge_dicts_0():
    import utool as ut
    x = {'a': 1, 'b': 2}
    y = {'b': 3, 'c': 4}
    mergedict_ = merge_dicts(x, y)
    result = ut.dict_str(mergedict_, sorted_=True, newlines=False)
    print(result)
    assert str(result) == u"{'a': 1, 'b': 3, 'c': 4}"


def test_move_odict_item_0():
    import utool as ut
    odict = OrderedDict()
    odict['a'] = 1
    odict['b'] = 2
    odict['c'] = 3
    odict['e'] = 5
    print(ut.dict_str(odict, nl=False))
    move_odict_item(odict, 'c', 1)
    print(ut.dict_str(odict, nl=False))
    move_odict_item(odict, 'a', 3)
    print(ut.dict_str(odict, nl=False))
    move_odict_item(odict, 'a', 0)
    print(ut.dict_str(odict, nl=False))
    move_odict_item(odict, 'b', 2)
    result = ut.dict_str(odict, nl=False)
    print(result)
    assert str(result) == u"{'a': 1, 'c': 3, 'b': 2, 'e': 5}"


def test_order_dict_by_0():
    import utool as ut
    dict_ = {1: 1, 2: 2, 3: 3, 4: 4}
    key_order = [4, 2, 3, 1]
    sorted_dict = order_dict_by(dict_, key_order)
    result = ('sorted_dict = %s' % (ut.dict_str(sorted_dict, nl=False),))
    print(result)
    assert str(result) == u'sorted_dict = {4: 4, 2: 2, 3: 3, 1: 1}'


def test_update_existing_0():
    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'a': 2, 'd': 3}
    dict1_ = update_existing(dict1, dict2)
    assert 'd' not in dict1
    assert dict1['a'] == 2
    assert dict1_ is dict1


def test_get_nonconflicting_string_0():
    # build test data
    base_fmtstr = 'somestring%d'
    conflict_set = ['somestring0']
    # execute function
    result = get_nonconflicting_string(base_fmtstr, conflict_set)
    # verify results
    print(result)
    assert str(result) == u'somestring1'


def test_get_object_size_0():
    import numpy as np
    import utool as ut
    obj = [np.empty(1, dtype=np.uint8) for _ in range(8)]
    nBytes = ut.get_object_nbytes(obj)
    result = ('nBytes = %s' % (nBytes,))
    print(result)
    assert str(result) == u'nBytes = 8'


def test_get_object_size_str_0():
    import numpy as np
    import utool as ut
    obj = [np.empty((512), dtype=np.uint8) for _ in range(10)]
    nBytes = ut.get_object_size_str(obj)
    result = ('result = %s' % (ut.repr2(nBytes),))
    print(result)
    assert str(result) == u"result = '5.00 KB'"


def test_get_stats_0():
    import numpy as np
    import utool
    axis = 0
    np.random.seed(0)
    list_ = np.random.rand(10, 2).astype(np.float32)
    stat_dict = get_stats(list_, axis, use_nan=False)
    result = str(utool.dict_str(stat_dict))
    print(result)
    assert str(result) == u"{\n    'max': np.array([ 0.96366274,  0.92559665], dtype=np.float32),\n    'min': np.array([ 0.0202184,  0.0871293], dtype=np.float32),\n    'mean': np.array([ 0.52056623,  0.64254338], dtype=np.float32),\n    'std': np.array([ 0.28543401,  0.25168759], dtype=np.float32),\n    'nMin': np.array([1, 1], dtype=np.int32),\n    'nMax': np.array([1, 1], dtype=np.int32),\n    'shape': (10, 2),\n}"


def test_get_stats_1():
    import numpy as np
    import utool
    axis = 0
    rng = np.random.RandomState(0)
    list_ = rng.randint(0, 42, size=100).astype(np.float32)
    list_[4] = np.nan
    stat_dict = get_stats(list_, axis, use_nan=True)
    result = str(utool.dict_str(stat_dict))
    print(result)
    assert str(result) == u"{\n    'max': 41.0,\n    'min': 0.0,\n    'mean': 20.0,\n    'std': 13.177115,\n    'nMin': 7,\n    'nMax': 3,\n    'shape': (100,),\n    'num_nan': 1,\n}"


def test_get_stats_2():
    import numpy as np
    import utool
    axis = 0
    rng = np.random.RandomState(0)
    list_ = rng.randint(0, 42, size=100).astype(np.int32)
    stat_dict = get_stats(list_, axis, use_nan=True)
    result = str(utool.dict_str(stat_dict))
    print(result)
    assert str(result) == u"{\n    'max': 41,\n    'min': 0,\n    'mean': 19.889999,\n    'std': 13.156668,\n    'nMin': 7,\n    'nMax': 3,\n    'shape': (100,),\n    'num_nan': 0,\n}"


def test_get_stats_str_0():
    list_ = [1, 2, 3, 4, 5]
    newlines = False
    keys = None
    exclude_keys = []
    lbl = None
    precision = 2
    stat_str = get_stats_str(list_, newlines, keys, exclude_keys, lbl, precision)
    result = str(stat_str)
    print(result)
    assert str(result) == u"{'max': 5, 'min': 1, 'mean': 3, 'std': 1.41, 'nMin': 1, 'nMax': 1, 'shape': (5,)}"


def test_make_at_least_n_items_valid_0():
    # build test data
    flag_list = [False, True, False, False, False, False, False, True]
    n = 5
    # execute function
    flag_list = make_at_least_n_items_valid(flag_list, n)
    # verify results
    result = str(flag_list)
    print(result)
    assert str(result) == u'[ True  True  True  True False False False  True]'


def test_print_stats_0():
    list_ = [1, 2, 3, 4, 5]
    lbl = None
    newlines = False
    precision = 2
    result = print_stats(list_, lbl, newlines, precision)
    assert str(result) == u"{'max': 5, 'min': 1, 'mean': 3, 'std': 1.41, 'nMin': 1, 'nMax': 1, 'shape': (5,)}"


def test_search_module_0():
    import utool as ut
    recursive = True
    ignore_case = True
    modname = ut.get_argval('--mod', type_=str, default='utool')
    pat = ut.get_argval('--pat', type_=str, default='search')
    mod = ut.import_modname(modname)
    print('pat = %r' % (pat,))
    print('mod = %r' % (mod,))
    found_list = search_module(mod, pat, recursive=recursive)
    result = ('found_list = %s' % (ut.repr2(found_list),))
    print(result)


def test_timeit_compare_0():
    import utool as ut
    setup = ut.codeblock(
        '''
        import numpy as np
        rng = np.random.RandomState(0)
        invVR_mats = rng.rand(1000, 3, 3).astype(np.float64)
        ''')
    stmt1 = 'invVR_mats[:, 0:2, 2].T'
    stmt2 = 'invVR_mats.T[2, 0:2]'
    iterations = 1000
    verbose = True
    stmt_list = [stmt1, stmt2]
    ut.timeit_compare(stmt_list, setup=setup, iterations=iterations, verbose=verbose)


def test_Timer_0():
    import utool
    with utool.Timer('Timer test!'):
        prime = utool.get_nth_prime(400)


def test_determine_timestamp_format_0():
    import utool as ut
    datetime_str_list = [
        '0000:00:00 00:00:00',
        '    :  :     :  :  ',
        '2015:04:01 00:00:00',
        '2080/04/01 00:00:00',
        '2005-10-27T14:35:20+02:00',
        '6:35:01\x002006:03:19 1',
        '2016/05/03 16:34:57 EST'
    ]
    result = ut.list_str([determine_timestamp_format(datetime_str)
               for datetime_str in datetime_str_list])
    print(result)


def test_exiftime_to_unixtime_0():
    datetime_str = '0000:00:00 00:00:00'
    timestamp_format = 1
    result = exiftime_to_unixtime(datetime_str, timestamp_format)
    print(result)
    assert str(result) == u'-1'


def test_exiftime_to_unixtime_1():
    datetime_str = '2015:04:01 00:00:00'
    timestamp_format = 1
    result = exiftime_to_unixtime(datetime_str, timestamp_format)
    print(result)
    assert str(result) == u'1427846400'


def test_exiftime_to_unixtime_2():
    datetime_str = '2005-10-27T14:35:20+02:00'
    timestamp_format = None
    result = exiftime_to_unixtime(datetime_str, timestamp_format)
    print(result)
    assert str(result) == u'1130423720'


def test_exiftime_to_unixtime_3():
    datetime_str = '6:35:01\x002006:03:19 1'
    timestamp_format = None
    result = exiftime_to_unixtime(datetime_str, timestamp_format)
    print(result)
    assert str(result) == u'1142750101'


def test_get_posix_timedelta_str_0():
    import utool as ut
    posixtime_list = [-13, 10.2, 10.2 ** 2, 10.2 ** 3, 10.2 ** 4, 10.2 ** 5, 10.2 ** 8, 60 * 60 * 60 * 24 * 7]
    posixtime = posixtime_list[-1]
    timedelta_str = [get_posix_timedelta_str(posixtime) for posixtime in posixtime_list]
    result = ut.repr2(timedelta_str)
    print(result)
    assert str(result) == u"['-00:00:13', '00:00:10', '00:01:44', '00:17:41', '03:00:24', '1 day', '193 weeks', '60 weeks']"


def test_get_timedelta_str_0():
    timedelta = get_unix_timedelta(10)
    timedelta_str = get_timedelta_str(timedelta)
    result = (timedelta_str)
    print(result)
    assert str(result) == u'10 seconds'


def test_get_timestamp_0():
    format_ = 'printable'
    use_second = False
    delta_seconds = None
    stamp = get_timestamp(format_, use_second, delta_seconds)
    print(stamp)
    assert len(stamp) == len('15:43:04 2015/02/24')


def test_get_timestats_str_0():
    import utool as ut
    unixtime_list = [0, 0 + 60 * 60 * 5 , 10 + 60 * 60 * 5, 100 + 60 * 60 * 5, 1000 + 60 * 60 * 5]
    newlines = True
    full = False
    timestat_str = get_timestats_str(unixtime_list, newlines, full=full, isutc=True)
    result = ut.align(str(timestat_str), ':')
    print(result)
    assert str(result) == u"{\n    'max'  : '1970/01/01 05:16:40',\n    'mean' : '1970/01/01 04:03:42',\n    'min'  : '1970/01/01 00:00:00',\n    'range': '5:16:40',\n    'std'  : '2:02:01',\n}"


def test_get_timestats_str_1():
    import utool as ut
    unixtime_list = [0, 0 + 60 * 60 * 5 , 10 + 60 * 60 * 5, 100 + 60 * 60 * 5, 1000 + 60 * 60 * 5, float('nan'), 0]
    newlines = True
    timestat_str = get_timestats_str(unixtime_list, newlines, isutc=True)
    result = ut.align(str(timestat_str), ':')
    print(result)
    assert str(result) == u"{\n    'max'    : '1970/01/01 05:16:40',\n    'mean'   : '1970/01/01 03:23:05',\n    'min'    : '1970/01/01 00:00:00',\n    'nMax'   : 1,\n    'nMin'   : 2,\n    'num_nan': 1,\n    'range'  : '5:16:40',\n    'shape'  : (7,),\n    'std'    : '2:23:43',\n}"


def test_get_unix_timedelta_str_0():
    import utool as ut
    unixtime_diff = 0
    timestr = get_unix_timedelta_str(unixtime_diff)
    timestr_list = [get_unix_timedelta_str(_) for _ in [-9001, -1, 0, 1, 9001]]
    result = ut.repr2(timestr_list)
    print(result)
    assert str(result) == u"['2 hours 30 minutes 1 second', '1 second', '0 seconds', '1 second', '2 hours 30 minutes 1 second']"


def test_parse_timedelta_str_0():
    str_ = '24h'
    timedelta = parse_timedelta_str(str_)
    result = ('timedelta = %s' % (str(timedelta),))
    print(result)
    assert str(result) == u'timedelta = 86400.0'


def test_parse_timestamp_0():
    import utool as ut
    utc = True
    timestampe_format = None
    timestamps = [
        ('2015:04:01 00:00:00',),
        ('2005-10-27T14:35:20+02:00',),
        ('2000-01-01T09:00:00-05:00', True),
        ('2000-01-01T09:00:00-05:00', False),
        ('2000-01-01T09:00:00', False),
        ('2000-01-01T09:00:00', True),
        ('6:35:01\x002006:03:19 1',),
        ('2016/08/18 10:51:02 EST',),
        ('2016-08-18T10:51:02-05:00',),
    ]
    timestamp = timestamps[-1][0]
    dn_list = [parse_timestamp(*args) for args in timestamps]
    result = ut.NEWLINE.join([str(dn) for dn in dn_list])
    print(result)
    assert str(result) == u'2015-04-01 00:00:00+00:00\n2005-10-27 12:35:20+00:00\n2000-01-01 14:00:00+00:00\n2000-01-01 09:00:00-05:00\n2000-01-01 09:00:00-05:00\n2000-01-01 09:00:00+00:00\n2006-03-19 06:35:01+00:00\n2016-08-18 15:51:02+00:00\n2016-08-18 15:51:02+00:00'


def test_is_int_0():
    var1 = 1
    var2 = np.array([1, 2, 3])
    var3 = True
    var4 = np.array([True, True, False])
    result = [is_int(var) for var in [var1, var2, var3, var4]]
    print(result)
    assert str(result) == u'[True, True, False, False]'


def test_smart_cast_0():
    var = '1'
    type_ = 'fuzzy_subset'
    cast_var = smart_cast(var, type_)
    result = repr(cast_var)
    print(result)
    assert str(result) == u'[1]'


def test_smart_cast_1():
    import utool as ut
    cast_var = smart_cast('1', None)
    result = ut.repr2(cast_var)
    print(result)
    assert str(result) == u"'1'"


def test_smart_cast_2():
    cast_var = smart_cast('(1,3)', 'eval')
    result = repr(cast_var)
    print(result)
    assert str(result) == u'(1, 3)'


def test_smart_cast_3():
    cast_var = smart_cast('(1,3)', eval)
    result = repr(cast_var)
    print(result)
    assert str(result) == u'(1, 3)'


def test_smart_cast_4():
    cast_var = smart_cast('1::3', slice)
    result = repr(cast_var)
    print(result)
    assert str(result) == u'slice(1, None, 3)'


def test_smart_cast2_0():
    import utool as ut
    # build test data
    var_list = ['?', 1, '1', '1.0', '1.2', 'True', None, 'None']
    # execute function
    castvar_list = [smart_cast2(var) for var in var_list]
    # verify results
    result = ut.list_str(castvar_list, nl=False)
    print(result)
    assert str(result) == u"['?', 1, 1, 1.0, 1.2, True, None, None]"


def test_make_csv_table_0():
    column_list = [[1, 2, 3], ['A', 'B', 'C']]
    column_lbls = ['num', 'alpha']
    header = '# Test CSV'
    column_type = (int, str)
    row_lbls = None
    transpose = False
    csv_text = make_csv_table(column_list, column_lbls, header, column_type, row_lbls, transpose)
    result = csv_text
    print(result)
    assert str(result) == u'# Test CSV\n# num_rows=3\n#   num,  alpha\n      1,      A\n      2,      B\n      3,      C'


def test_ichunks_0():
    iterable = [1, 2, 3, 4, 5, 6, 7]
    chunksize = 3
    genresult = ichunks(iterable, chunksize)
    result = list(genresult)
    print(result)
    assert str(result) == u'[[1, 2, 3], [4, 5, 6], [7]]'


def test_ichunks_1():
    iterable = (1, 2, 3, 4, 5, 6, 7)
    chunksize = 3
    bordermode = 'cycle'
    genresult = ichunks(iterable, chunksize, bordermode)
    result = list(genresult)
    print(result)
    assert str(result) == u'[[1, 2, 3], [4, 5, 6], [7, 1, 2]]'


def test_ichunks_2():
    iterable = (1, 2, 3, 4, 5, 6, 7)
    chunksize = 3
    bordermode = 'replicate'
    genresult = ichunks(iterable, chunksize, bordermode)
    result = list(genresult)
    print(result)
    assert str(result) == u'[[1, 2, 3], [4, 5, 6], [7, 7, 7]]'


def test_ifilterfalse_items_0():
    item_iter = [1, 2, 3, 4, 5]
    flag_iter = [False, True, True, False, True]
    false_items = ifilterfalse_items(item_iter, flag_iter)
    result = list(false_items)
    print(result)
    assert str(result) == u'[1, 4]'


def test_interleave_0():
    import utool as ut
    args = ([1, 2, 3, 4, 5], ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    genresult = interleave(args)
    result = ut.list_str(list(genresult), nl=False)
    print(result)
    assert str(result) == u"[1, 'A', 2, 'B', 3, 'C', 4, 'D', 5, 'E']"


def test_iter_compress_0():
    item_iter = [1, 2, 3, 4, 5]
    flag_iter = [False, True, True, False, True]
    true_items = iter_compress(item_iter, flag_iter)
    result = list(true_items)
    print(result)
    assert str(result) == u'[2, 3, 5]'


def test_iter_multichunks_0():
    import utool as ut
    iterable = list(range(20))
    chunksizes = (3, 2, 3)
    bordermode = 'cycle'
    genresult = iter_multichunks(iterable, chunksizes, bordermode)
    multichunks = list(genresult)
    depthprofile = ut.depth_profile(multichunks)
    assert depthprofile[1:] == chunksizes, 'did not generate chunks correctly'
    result = ut.list_str(map(str, multichunks), nobr=True)
    print(result)
    assert str(result) == u"'[[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [9, 10, 11]], [[12, 13, 14], [15, 16, 17]]]',\n'[[[18, 19, 0], [1, 2, 3]], [[4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15]]]',"


def test_iter_multichunks_1():
    import utool as ut
    iterable = list(range(7))
    # when chunksizes is len == 1, then equlivalent to ichunks
    chunksizes = (3,)
    bordermode = 'cycle'
    genresult = iter_multichunks(iterable, chunksizes, bordermode)
    multichunks = list(genresult)
    depthprofile = ut.depth_profile(multichunks)
    assert depthprofile[1:] == chunksizes, 'did not generate chunks correctly'
    result = str(multichunks)
    print(result)
    assert str(result) == u'[[0, 1, 2], [3, 4, 5], [6, 0, 1]]'


def test_iter_window_0():
    iterable = [1, 2, 3, 4, 5, 6]
    size, step, wrap = 3, 1, True
    window_iter = iter_window(iterable, size, step, wrap)
    window_list = list(window_iter)
    result = ('window_list = %r' % (window_list,))
    print(result)
    assert str(result) == u'window_list = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 1), (6, 1, 2)]'


def test_iter_window_1():
    iterable = [1, 2, 3, 4, 5, 6]
    size, step, wrap = 3, 2, True
    window_iter = iter_window(iterable, size, step, wrap)
    window_list = list(window_iter)
    result = ('window_list = %r' % (window_list,))
    print(result)
    assert str(result) == u'window_list = [(1, 2, 3), (3, 4, 5), (5, 6, 1)]'


def test_itertwo_0():
    iterable = [1, 2, 3, 4]
    wrap = False
    edges = list(itertwo(iterable, wrap))
    result = ('edges = %r' % (edges,))
    print(result)
    assert str(result) == u'edges = [(1, 2), (2, 3), (3, 4)]'


def test_itertwo_1():
    iterable = [1, 2, 3, 4]
    wrap = True
    edges = list(itertwo(iterable, wrap))
    result = ('edges = %r' % (edges,))
    print(result)
    assert str(result) == u'edges = [(1, 2), (2, 3), (3, 4), (4, 1)]'


def test_itertwo_2():
    import utool as ut
    iterable = iter([1, 2, 3, 4])
    wrap = False
    edge_iter = itertwo(iterable, wrap)
    edges = list(edge_iter)
    result = ('edges = %r' % (edges,))
    ut.assert_eq(len(list(iterable)), 0, 'iterable should have been used up')
    print(result)
    assert str(result) == u'edges = [(1, 2), (2, 3), (3, 4)]'


def test_next_counter_0():
    start = 1
    step = 1
    next_ = next_counter(start, step)
    result = str([next_(), next_(), next_()])
    print(result)
    assert str(result) == u'[1, 2, 3]'


def test_filterflags_general_tags_0():
    import utool as ut
    tags_list = [['v'], [], ['P'], ['P', 'o'], ['n', 'o'], [], ['n', 'N'], ['e', 'i', 'p', 'b', 'n'], ['q', 'v'], ['n'], ['n'], ['N']]
    kwargs = ut.argparse_dict(ut.get_kwdefaults2(filterflags_general_tags), type_hint=list)
    print('kwargs = %r' % (kwargs,))
    flags = filterflags_general_tags(tags_list, **kwargs)
    print(flags)
    result = ut.compress(tags_list, flags)
    print('result = %r' % (result,))


def test_filterflags_general_tags_1():
    import utool as ut
    tags_list = [['v'], [], ['P'], ['P'], ['n', 'o'], [], ['n', 'N'], ['e', 'i', 'p', 'b', 'n'], ['n'], ['n'], ['N']]
    has_all = 'n'
    min_num = 1
    flags = filterflags_general_tags(tags_list, has_all=has_all, min_num=min_num)
    result = ut.compress(tags_list, flags)
    print('result = %r' % (result,))


def test_filterflags_general_tags_2():
    import utool as ut
    tags_list = [['vn'], ['vn', 'no'], ['P'], ['P'], ['n', 'o'], [], ['n', 'N'], ['e', 'i', 'p', 'b', 'n'], ['n'], ['n', 'nP'], ['NP']]
    kwargs = {
        'any_endswith': 'n',
        'any_match': None,
        'any_startswith': 'n',
        'has_all': None,
        'has_any': None,
        'has_none': None,
        'max_num': 3,
        'min_num': 1,
        'none_match': ['P'],
    }
    flags = filterflags_general_tags(tags_list, **kwargs)
    filtered = ut.compress(tags_list, flags)
    result = ('result = %s' % (ut.repr2(filtered),))
    assert str(result) == u"result = [['vn', 'no'], ['n', 'o'], ['n', 'N'], ['n'], ['n', 'nP']]"


def test_Indenter_0():
    import utool as ut
    ut.util_print._test_indent_print()


def test_get_arg_dict_0():
    import utool as ut
    import shlex
    argv = shlex.split('--test-show_name --name=IBEIS_PZ_0303 --db testdb3 --save "~/latex/crall-candidacy-2015/figures/IBEIS_PZ_0303.jpg" --dpath figures --caption="Shadowed"  --figsize=11,3 --no-figtitle -t foo bar baz biz --notitle')
    arg_dict = ut.get_arg_dict(argv, prefix_list=['--', '-'], type_hints={'t': list})
    result = ut.dict_str(arg_dict)
    # verify results
    print(result)
    assert str(result) == u"{\n    'caption': 'Shadowed',\n    'db': 'testdb3',\n    'dpath': 'figures',\n    'figsize': '11,3',\n    'name': 'IBEIS_PZ_0303',\n    'no-figtitle': True,\n    'notitle': True,\n    'save': '~/latex/crall-candidacy-2015/figures/IBEIS_PZ_0303.jpg',\n    't': ['foo', 'bar', 'baz', 'biz'],\n    'test-show_name': True,\n}"


def test_get_argv_tail_0():
    import utool as ut
    from os.path import relpath, dirname
    scriptname = 'utool.util_arg'
    prefer_main = False
    argv=['python', '-m', 'utool.util_arg', '--test-get_argv_tail']
    tail = get_argv_tail(scriptname, prefer_main, argv)
    # hack
    tail[0] = ut.ensure_unixslash(relpath(tail[0], dirname(dirname(ut.__file__))))
    result = ut.repr2(tail)
    print(result)
    assert str(result) == u"['utool/util_arg.py', '--test-get_argv_tail']"


def test_get_argv_tail_1():
    import utool as ut
    from os.path import relpath, dirname
    scriptname = 'utprof.py'
    prefer_main = True
    argv=['utprof.py', '-m', 'utool', '--tf', 'get_argv_tail']
    tail = get_argv_tail(scriptname, prefer_main, argv)
    # hack
    tail[0] = ut.ensure_unixslash(relpath(tail[0], dirname(dirname(ut.__file__))))
    result = ut.repr2(tail)
    print(result)
    assert str(result) == u"['utool/__main__.py', '--tf', 'get_argv_tail']"


def test_get_argval_0():
    import utool as ut
    import sys
    argv = ['--spam', 'eggs', '--quest=holy grail', '--ans=42', '--the-val=1,2,3']
    # specify a list of args and kwargs to get_argval
    argstr_kwargs_list = [
        ('--spam',                    dict(type_=str, default=None, argv=argv)),
        ('--quest',                   dict(type_=str, default=None, argv=argv)),
        (('--ans', '--foo'),          dict(type_=int, default=None, argv=argv)),
        (('--not-there', '--absent'), dict(argv=argv)),
        ('--the_val',                 dict(type_=list, argv=argv)),
        ('--the-val',                 dict(type_=list, argv=argv)),
    ]
    # Execute the command with for each of the test cases
    res_list = []
    argstr_list = ut.get_list_column(argstr_kwargs_list, 0)
    for argstr_, kwargs in argstr_kwargs_list:
        res = get_argval(argstr_, **kwargs)
        res_list.append(res)
    result = ut.dict_str(ut.odict(zip(argstr_list, res_list)))
    result = result.replace('u\'', '\'')  # hack
    print(result)
    assert str(result) == u"{\n    '--spam': 'eggs',\n    '--quest': 'holy grail',\n    ('--ans', '--foo'): 42,\n    ('--not-there', '--absent'): None,\n    '--the_val': [1, 2, 3],\n    '--the-val': [1, 2, 3],\n}"


def test_get_argval_1():
    import utool as ut
    import sys
    argv = ['--slice1', '::', '--slice2=4:', '--slice3=::4', '--slice4', '[1,2,3,4]', '--slice5=3']
    # specify a list of args and kwargs to get_argval
    argstr_kwargs_list = [
        ('--slice1',            dict(type_='fuzzy_subset', default=None, argv=argv)),
        ('--slice2',            dict(type_='fuzzy_subset', default=None, argv=argv)),
        ('--slice3',            dict(type_='fuzzy_subset', default=None, argv=argv)),
        ('--slice4',            dict(type_='fuzzy_subset', default=None, argv=argv)),
        ('--slice5',            dict(type_='fuzzy_subset', default=None, argv=argv)),
    ]
    # Execute the command with for each of the test cases
    res_list = []
    argstr_list = ut.get_list_column(argstr_kwargs_list, 0)
    list1 = [1, 3, 5, 7, 9]
    import numpy as np
    list2 = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 1]])
    for argstr_, kwargs in argstr_kwargs_list:
        res = get_argval(argstr_, **kwargs)
        print('---')
        print('res = %r' % (res,))
        print('list1[%r=%r] = %r' % (argstr_, res, ut.take(list1, res),))
        print('list2[%r=%r] = %r' % (argstr_, res, list2[res].tolist(),))
        res_list.append(res)
    result = ut.dict_str(ut.odict(zip(argstr_list, res_list)))
    result = result.replace('u\'', '\'')  # hack
    print(result)


def test_parse_cfgstr_list_0():
    import utool as ut
    cfgstr_list = ['var1=val1', 'var2=1', 'var3=1.0', 'var4=None', 'var5=[1,2,3]', 'var6=(a,b,c)']
    smartcast = True
    cfgdict = parse_cfgstr_list(cfgstr_list, smartcast, oldmode=False)
    result = ut.repr2(cfgdict, sorted_=True, newlines=False)
    print(result)
    assert str(result) == u"{'var1': 'val1', 'var2': 1, 'var3': 1.0, 'var4': None, 'var5': [1, 2, 3], 'var6': ('a', 'b', 'c')}"


def test_longest_levels_0():
    import utool as ut
    levels_ = [
        ['dummy_annot'],
        ['chip', 'probchip'],
        ['keypoint', 'fgweight'],
        ['fgweight'],
    ]
    new_levels = longest_levels(levels_)
    result = ('new_levels = %s' % (ut.repr2(new_levels, nl=1),))
    print(result)
    assert str(result) == u"new_levels = [\n    ['dummy_annot'],\n    ['chip', 'probchip'],\n    ['keypoint'],\n    ['fgweight'],\n]"


def test_nx_dag_node_rank_0():
    import utool as ut
    adj_dict = {0: [5], 1: [5], 2: [1], 3: [4], 4: [0], 5: [], 6: [4], 7: [9], 8: [6], 9: [1]}
    import networkx as nx
    nodes = [2, 1, 5]
    f_graph = ut.nx_from_adj_dict(adj_dict, nx.DiGraph)
    graph = f_graph.reverse()
    #ranks = ut.nx_dag_node_rank(graph, nodes)
    ranks = ut.nx_dag_node_rank(graph, nodes)
    result = ('ranks = %r' % (ranks,))
    print(result)
    assert str(result) == u'ranks = [3, 2, 1]'


def test_paths_to_root_0():
    import utool as ut
    child_to_parents = {
        'chip': ['dummy_annot'],
        'chipmask': ['dummy_annot'],
        'descriptor': ['keypoint'],
        'fgweight': ['keypoint', 'probchip'],
        'keypoint': ['chip'],
        'notch': ['dummy_annot'],
        'probchip': ['dummy_annot'],
        'spam': ['fgweight', 'chip', 'keypoint']
    }
    root = 'dummy_annot'
    tablename = 'fgweight'
    to_root = paths_to_root(tablename, root, child_to_parents)
    result = ut.repr3(to_root)
    print(result)
    assert str(result) == u"{\n    'keypoint': {\n        'chip': {\n                'dummy_annot': None,\n            },\n    },\n    'probchip': {\n        'dummy_annot': None,\n    },\n}"


def test_reverse_path_0():
    import utool as ut
    child_to_parents = {
        'chip': ['dummy_annot'],
        'chipmask': ['dummy_annot'],
        'descriptor': ['keypoint'],
        'fgweight': ['keypoint', 'probchip'],
        'keypoint': ['chip'],
        'notch': ['dummy_annot'],
        'probchip': ['dummy_annot'],
        'spam': ['fgweight', 'chip', 'keypoint']
    }
    to_root = {
        'fgweight': {
            'keypoint': {
                'chip': {
                    'dummy_annot': None,
                },
            },
            'probchip': {
                'dummy_annot': None,
            },
        },
    }
    reversed_ = reverse_path(to_root, 'dummy_annot', child_to_parents)
    result = ut.repr3(reversed_)
    print(result)
    assert str(result) == u"{\n    'dummy_annot': {\n        'chip': {\n                'keypoint': {\n                            'fgweight': None,\n                        },\n            },\n        'probchip': {\n                'fgweight': None,\n            },\n    },\n}"


def test_shortest_levels_0():
    import utool as ut
    levels_ = [
        ['dummy_annot'],
        ['chip', 'probchip'],
        ['keypoint', 'fgweight'],
        ['fgweight'],
    ]
    new_levels = shortest_levels(levels_)
    result = ('new_levels = %s' % (ut.repr2(new_levels, nl=1),))
    print(result)
    assert str(result) == u"new_levels = [\n    ['dummy_annot'],\n    ['chip', 'probchip'],\n    ['keypoint', 'fgweight'],\n]"


def test_simplify_graph_0():
    import utool as ut
    import networkx as nx
    graph = nx.DiGraph([('a', 'b'), ('a', 'c'), ('a', 'e'),
                        ('a', 'd'), ('b', 'd'), ('c', 'e'),
                        ('d', 'e'), ('c', 'e'), ('c', 'd')])
    new_graph = simplify_graph(graph)
    result = ut.repr2(list(new_graph.edges()))
    #adj_list = sorted(list(nx.generate_adjlist(new_graph)))
    #result = ut.repr2(adj_list)
    print(result)
    assert str(result) == u'[(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (2, 3), (2, 4), (3, 4)]'


def test_check_module_installed_0():
    import utool as ut
    modname = ut.get_argval('--modname', default='this')
    is_installed = check_module_installed(modname)
    is_imported = modname in sys.modules
    print('module(%r).is_installed = %r' % (modname, is_installed))
    print('module(%r).is_imported = %r' % (modname, is_imported))
    assert 'this' not in sys.modules, 'module(this) should not have ever been imported'


def test_import_modname_0():
    modname_list = [
        'utool',
        'utool._internal',
        'utool._internal.meta_util_six',
        'utool.util_path',
        #'utool.util_path.checkpath',
    ]
    modules = [import_modname(modname) for modname in modname_list]
    result = ([m.__name__ for m in modules])
    assert result == modname_list


def test_tryimport_0():
    import utool as ut
    modname = 'pyfiglet'
    pipiname = 'git+https://github.com/pwaller/pyfiglet'
    pyfiglet = ut.tryimport(modname, pipiname)
    assert pyfiglet is None or isinstance(pyfiglet, types.ModuleType), 'unknown error'


def test_generate_0():
    import utool as ut
    #num = 8700  # parallel is slower for smaller numbers
    num = 500  # parallel has an initial (~.1 second startup overhead)
    print('TESTING SERIAL')
    func = ut.is_prime
    args_list = list(range(0, num))
    flag_generator0 = ut.generate(ut.is_prime, range(0, num), force_serial=True, freq=num / 4)
    flag_list0 = list(flag_generator0)
    print('TESTING PARALLEL')
    flag_generator1 = ut.generate(ut.is_prime, range(0, num), freq=num / 10)
    flag_list1 = list(flag_generator1)
    print('ASSERTING')
    assert len(flag_list1) == num
    assert flag_list0 == flag_list1


def test_generate_1():
    # Trying to recreate the freeze seen in IBEIS
    import utool as ut
    print('TESTING SERIAL')
    flag_generator0 = ut.generate(ut.is_prime, range(0, 1))
    flag_list0 = list(flag_generator0)
    flag_generator1 = ut.generate(ut.fibonacci_recursive, range(0, 1))
    flag_list1 = list(flag_generator1)
    print('TESTING PARALLEL')
    flag_generator2 = ut.generate(ut.is_prime, range(0, 12))
    flag_list2 = list(flag_generator2)
    flag_generator3 = ut.generate(ut.fibonacci_recursive, range(0, 12))
    flag_list3 = list(flag_generator3)
    print('flag_list0 = %r' % (flag_list0,))
    print('flag_list1 = %r' % (flag_list1,))
    print('flag_list2 = %r' % (flag_list1,))
    print('flag_list3 = %r' % (flag_list1,))


def test_cmd_0():
    import utool as ut
    (out, err, ret) = ut.cmd('echo', 'hello world')
    result = ut.list_str(list(zip(('out', 'err', 'ret'), (out, err, ret))), nobraces=True)
    print(result)
    assert str(result) == u"('out', 'hello world\\n'),\n('err', None),\n('ret', 0),"


def test_cmd_1():
    import utool as ut
    target = ut.codeblock(
         r'''
         ('out', 'hello world\n'),
         ('err', None),
         ('ret', 0),
         ''')
    varydict = {
       'shell': [True, False],
       'detatch': [False],
       'sudo': [True, False] if ut.get_argflag('--test-sudo') else [False],
       'args': ['echo hello world', ('echo', 'hello world')],
    }
    for count, kw in enumerate(ut.all_dict_combinations(varydict), start=1):
        print('+ --- TEST CMD %d ---' % (count,))
        print('testing cmd with params ' + ut.dict_str(kw))
        args = kw.pop('args')
        restup = ut.cmd(args, pad_stdout=False, **kw)
        tupfields = ('out', 'err', 'ret')
        output = ut.list_str(list(zip(tupfields, restup)), nobraces=True)
        ut.assert_eq(output, target)
        print('L ___ TEST CMD %d ___\n' % (count,))


def test_get_free_diskbytes_0():
    import utool as ut
    dir_ = ut.get_argval('--dir', type_=str, default=ut.truepath('~'))
    bytes_ = get_free_diskbytes(dir_)
    result = ('bytes_ = %s' % (str(bytes_),))
    print(result)
    print('Unused space in %r = %r' % (dir_, ut.byte_str2(bytes_)))
    print('Total space in %r = %r' % (dir_, ut.byte_str2(get_total_diskbytes(dir_))))


def test_python_executable_0():
    short = False
    result = python_executable(short)
    print(result)


def test_align_0():
    character = '='
    text = 'a = b=\none = two\nthree = fish\n'
    print(text)
    result = (align(text, '='))
    print(result)
    assert str(result) == u'a     = b=\none   = two\nthree = fish'


def test_align_lines_0():
    line_list = 'a = b\none = two\nthree = fish'.split('\n')
    character = '='
    new_lines = align_lines(line_list, character)
    result = ('\n'.join(new_lines))
    print(result)
    assert str(result) == u'a     = b\none   = two\nthree = fish'


def test_align_lines_1():
    line_list = 'foofish:\n    a = b\n    one    = two\n    three    = fish'.split('\n')
    character = '='
    new_lines = align_lines(line_list, character)
    result = ('\n'.join(new_lines))
    print(result)
    assert str(result) == u'foofish:\n    a        = b\n    one      = two\n    three    = fish'


def test_align_lines_2():
    import utool as ut
    character = ':'
    text = ut.codeblock('''
    {'max': '1970/01/01 02:30:13',
     'mean': '1970/01/01 01:10:15',
     'min': '1970/01/01 00:01:41',
     'range': '2:28:32',
     'std': '1:13:57',}''').split('\n')
    new_lines = align_lines(text, ':', ' :')
    result = '\n'.join(new_lines)
    print(result)
    assert str(result) == u"{'max'   : '1970/01/01 02:30:13',\n 'mean'  : '1970/01/01 01:10:15',\n 'min'   : '1970/01/01 00:01:41',\n 'range' : '2:28:32',\n 'std'   : '1:13:57',}"


def test_bubbletext_0():
    import utool as ut
    bubble_text1 = ut.bubbletext('TESTING', font='cyberlarge')
    bubble_text2 = ut.bubbletext('BUBBLE', font='cybermedium')
    bubble_text3 = ut.bubbletext('TEXT', font='cyberlarge')
    print('\n'.join([bubble_text1, bubble_text2, bubble_text3]))


def test_byte_str2_0():
    import utool as ut
    nBytes_list = [1, 100, 1024,  1048576, 1073741824, 1099511627776]
    result = ut.list_str(list(map(byte_str2, nBytes_list)), nl=False)
    print(result)
    assert str(result) == u"['0.00 KB', '0.10 KB', '1.00 KB', '1.00 MB', '1.00 GB', '1.00 TB']"


def test_chr_range_0():
    import utool as ut
    args = (5,)
    result = ut.repr2(chr_range(2, base='a'))
    print(result)
    print(chr_range(0, 5))
    print(chr_range(0, 50))
    print(chr_range(0, 5, 2))
    assert str(result) == u"['a', 'b']"


def test_conj_phrase_0():
    list_ = ['a', 'b', 'c']
    result = conj_phrase(list_, 'or')
    print(result)
    assert str(result) == u'a, b, or c'


def test_conj_phrase_1():
    list_ = ['a', 'b']
    result = conj_phrase(list_, 'and')
    print(result)
    assert str(result) == u'a and b'


def test_dict_str_0():
    from utool.util_str import dict_str, dict_itemstr_list
    import utool as ut
    dict_ = {'foo': {'spam': 'barbarbarbarbar' * 3, 'eggs': 'jam'},
             'baz': 'barbarbarbarbar' * 3}
    truncate = ut.get_argval('--truncate', type_=None, default=1)
    result = dict_str(dict_, strvals=True, truncate=truncate,
                       truncatekw={'maxlen': 20})
    print(result)
    assert str(result) == u"{\n    'baz': barbarbarbarbarbarbarbarbarbarbarbarbarbarbar,\n    'foo': {\n        'eggs': jam,\n        's ~~~TRUNCATED~~~ ,\n    },\n}"


def test_func_callsig_0():
    func = func_str
    callsig = func_callsig(func)
    result = str(callsig)
    print(result)
    assert str(result) == u'func_str(func, args, kwargs, type_aliases, packed, packkw, truncate)'


def test_func_defsig_0():
    func = func_str
    defsig = func_defsig(func)
    result = str(defsig)
    print(result)
    assert str(result) == u'func_str(func, args=[], kwargs={}, type_aliases=[], packed=False, packkw=None, truncate=False)'


def test_func_str_0():
    func = byte_str
    args = [1024, 'MB']
    kwargs = dict(precision=2)
    type_aliases = []
    packed = False
    packkw = None
    _str = func_str(func, args, kwargs, type_aliases, packed, packkw)
    result = _str
    print(result)
    assert str(result) == u"byte_str(1024, 'MB', precision=2)"


def test_get_callable_name_0():
    func = len
    result = get_callable_name(func)
    print(result)
    assert str(result) == u'len'


def test_horiz_string_0():
    # Pretty printing of matrices demo / test
    import utool
    import numpy as np
    # Wouldn't it be nice if we could print this operation easily?
    B = np.array(((1, 2), (3, 4)))
    C = np.array(((5, 6), (7, 8)))
    A = B.dot(C)
    # Eg 1:
    result = (utool.hz_str('A = ', A, ' = ', B, ' * ', C))
    print(result)
    assert str(result) == u'A = [[19 22]  = [[1 2]  * [[5 6]\n     [43 50]]    [3 4]]    [7 8]]'


def test_list_str_0():
    import utool as ut
    list_ = [[(('--verbose-qt', '--verbqt'), 1, False, ''),
              (('--verbose-qt', '--verbqt'), 1, False, ''),
              (('--verbose-qt', '--verbqt'), 1, False, ''),
              (('--verbose-qt', '--verbqt'), 1, False, '')],
             [(['--nodyn'], 1, False, ''), (['--nodyn'], 1, False, '')]]
    indent_ = ''
    newlines = 2
    truncate = ut.get_argval('--truncate', type_=None, default=False)
    nobraces = False
    nl = None
    result = list_str(list_, indent_, newlines, nobraces, nl,
                      truncate=truncate, truncatekw={'maxlen': 10})
    print(result)
    assert str(result) == u"[\n    [\n        (('--verbose-qt', '--verbqt'), 1, False, ''),\n        (('--verbose-qt', '--verbqt'), 1, False, ''),\n        (('--verbose-qt', '--verbqt'), 1, False, ''),\n        (('--verbose-qt', '--verbqt'), 1, False, ''),\n    ],\n    [\n        (['--nodyn'], 1, False, ''),\n        (['--nodyn'], 1, False, ''),\n    ],\n]"


def test_multi_replace_0():
    str_ = 'foo. bar: baz; spam-eggs --- eggs+spam'
    search_list = ['.', ':', '---']
    repl_list = '@'
    str_ = multi_replace(str_, search_list, repl_list)
    result = ('str_ = %s' % (str(str_),))
    print(result)
    assert str(result) == u'str_ = foo@ bar@ baz; spam-eggs @ eggs+spam'


def test_remove_chars_0():
    str_ = '1, 2, 3, 4'
    char_list = [',']
    result = remove_chars(str_, char_list)
    print(result)
    assert str(result) == u'1 2 3 4'


def test_seconds_str_0():
    import utool as ut
    num_list = sorted([4.2 / (10.0 ** exp_)
                       for exp_ in range(-13, 13, 4)])
    secstr_list = [seconds_str(num, prefix=None) for num in num_list]
    result = (', '.join(secstr_list))
    print(result)
    assert str(result) == u'0.04 ns, 0.42 us, 4.20 ms, 0.04 ks, 0.42 Ms, 4.20 Gs, 42.00 Ts'


def test_theta_str_0():
    theta = 3.1415
    result = theta_str(theta)
    print(result)
    assert str(result) == u'0.5*2pi'


def test_theta_str_1():
    theta = 6.9932
    taustr = 'tau'
    result = theta_str(theta, taustr)
    print(result)
    assert str(result) == u'1.1tau'


def test_to_camel_case_0():
    underscore_case = 'underscore_funcname'
    camel_case_str = to_camel_case(underscore_case)
    result = ('camel_case_str = %s' % (str(camel_case_str),))
    print(result)
    assert str(result) == u'camel_case_str = UnderscoreFuncname'


def test_to_underscore_case_0():
    camelcase_str = 'UnderscoreFuncname'
    camel_case_str = to_underscore_case(camelcase_str)
    result = ('underscore_str = %s' % (str(camel_case_str),))
    print(result)
    assert str(result) == u'underscore_str = underscore_funcname'


def test_GridSearch_0():
    import utool as ut
    grid_basis = [
        ut.DimensionBasis('p', [.5, .8, .9, 1.0]),
        ut.DimensionBasis('K', [2, 3, 4, 5]),
        ut.DimensionBasis('dcvs_clip_max', [.1, .2, .5, 1.0]),
    ]
    gridsearch = ut.GridSearch(grid_basis, label='testdata_gridsearch')
    for cfgdict in gridsearch:
        tp_score = cfgdict['p'] + (cfgdict['K'] ** .5)
        tn_score = (cfgdict['p'] * (cfgdict['K'])) / cfgdict['dcvs_clip_max']
        gridsearch.append_result(tp_score, tn_score)


def test_ParamInfoBool_0():
    import utool as ut
    pi = ParamInfoBool('cheese_on', hideif=util_dev.NoParam)
    cfg = ut.DynStruct()
    cfg.cheese_on = False
    result = pi.get_itemstr(cfg)
    print(result)
    assert str(result) == u'nocheese'


def test_ParamInfo___init___0():
    import utool as ut
    pi = ParamInfo(varname='foo', default='bar')
    cfg = ut.DynStruct()
    cfg.foo = 5
    result = pi.get_itemstr(cfg)
    print(result)
    assert str(result) == u'foo=5'


def test_customize_base_cfg_0():
    import utool as ut
    cfgname = 'name'
    cfgopt_strs = 'b=[1,2]'
    base_cfg = {}
    alias_keys = None
    cfgtype = None
    offset = 0
    valid_keys = None
    strict = False
    cfg_combo = customize_base_cfg(cfgname, cfgopt_strs, base_cfg, cfgtype,
                                   alias_keys, valid_keys, offset, strict)
    result = ('cfg_combo = %s' % (ut.repr2(cfg_combo, nl=1),))
    print(result)
    assert str(result) == u"cfg_combo = [\n    {'_cfgindex': 0, '_cfgname': 'name', '_cfgstr': 'name:b=[1,2]', '_cfgtype': None, 'b': 1},\n    {'_cfgindex': 1, '_cfgname': 'name', '_cfgstr': 'name:b=[1,2]', '_cfgtype': None, 'b': 2},\n]"


def test_get_cfg_lbl_0():
    import utool as ut
    cfg = {'_cfgname': 'test', 'var1': 'val1', 'var2': 'val2'}
    name = None
    nonlbl_keys = ['_cfgstr', '_cfgname', '_cfgtype', '_cfgindex']
    cfg_lbl = get_cfg_lbl(cfg, name, nonlbl_keys)
    result = ('cfg_lbl = %s' % (six.text_type(cfg_lbl),))
    print(result)
    assert str(result) == u'cfg_lbl = test:var1=val1,var2=val2'


def test_get_cfg_lbl_1():
    import utool as ut
    cfg = {'var1': 'val1', 'var2': 'val2'}
    default_cfg = {'var2': 'val1', 'var1': 'val1'}
    name = None
    cfg_lbl = get_cfg_lbl(cfg, name, default_cfg=default_cfg)
    result = ('cfg_lbl = %s' % (six.text_type(cfg_lbl),))
    print(result)
    assert str(result) == u'cfg_lbl = :var2=val2'


def test_get_cfg_lbl_2():
    import utool as ut
    cfg = {'_cfgname': 'test:K=[1,2,3]', 'K': '1'}
    name = None
    nonlbl_keys = ['_cfgstr', '_cfgname', '_cfgtype', '_cfgindex']
    cfg_lbl = get_cfg_lbl(cfg, name, nonlbl_keys)
    result = ('cfg_lbl = %s' % (six.text_type(cfg_lbl),))
    print(result)
    assert str(result) == u'cfg_lbl = test:K=1'


def test_get_cfgdict_list_subset_0():
    import utool as ut
    # build test data
    cfgdict_list = [
        {'K': 3, 'dcvs_clip_max': 0.1, 'p': 0.1},
        {'K': 5, 'dcvs_clip_max': 0.1, 'p': 0.1},
        {'K': 5, 'dcvs_clip_max': 0.1, 'p': 0.2},
        {'K': 3, 'dcvs_clip_max': 0.2, 'p': 0.1},
        {'K': 5, 'dcvs_clip_max': 0.2, 'p': 0.1},
        {'K': 3, 'dcvs_clip_max': 0.2, 'p': 0.1}]
    keys = ['K', 'dcvs_clip_max']
    # execute function
    cfgdict_sublist = get_cfgdict_list_subset(cfgdict_list, keys)
    # verify results
    result = ut.list_str(cfgdict_sublist)
    print(result)
    assert str(result) == u"[\n    {'K': 3, 'dcvs_clip_max': 0.1},\n    {'K': 5, 'dcvs_clip_max': 0.1},\n    {'K': 3, 'dcvs_clip_max': 0.2},\n    {'K': 5, 'dcvs_clip_max': 0.2},\n]"


def test_get_nonvaried_cfg_lbls_0():
    import utool as ut
    cfg_list = [{'_cfgname': 'test', 'f': 1, 'b': 1},
                {'_cfgname': 'test', 'f': 2, 'b': 1},
                {'_cfgname': 'test', 'f': 3, 'b': 1, 'z': 4}]
    default_cfg = None
    cfglbl_list = get_nonvaried_cfg_lbls(cfg_list, default_cfg)
    result = ('cfglbl_list = %s' % (ut.repr2(cfglbl_list),))
    print(result)
    assert str(result) == u"cfglbl_list = ['test:b=1', 'test:b=1', 'test:b=1']"


def test_get_varied_cfg_lbls_0():
    import utool as ut
    cfg_list = [{'_cfgname': 'test', 'f': 1, 'b': 1},
                {'_cfgname': 'test', 'f': 2, 'b': 1},
                {'_cfgname': 'test', 'f': 3, 'b': 1, 'z': 4}]
    default_cfg = None
    cfglbl_list = get_varied_cfg_lbls(cfg_list, default_cfg)
    result = ('cfglbl_list = %s' % (ut.repr2(cfglbl_list),))
    print(result)
    assert str(result) == u"cfglbl_list = ['test:f=1', 'test:f=2', 'test:f=3,z=4']"


def test_grid_search_generator_0():
    import utool as ut
    # build test data
    grid_basis = [
        DimensionBasis('dim1', [.1, .2, .3]),
        DimensionBasis('dim2', [.1, .4, .5]),
    ]
    args = tuple()
    kwargs = {}
    # execute function
    point_list = list(grid_search_generator(grid_basis))
    # verify results
    column_lbls = ut.get_list_column(grid_basis, 0)
    column_list  = ut.get_list_column(grid_basis, 1)
    first_vals = ut.get_list_column(ut.get_list_column(grid_basis, 1), 0)
    column_types = list(map(type, first_vals))
    header = 'grid search'
    result = ut.make_csv_table(column_list, column_lbls, header, column_types)
    print(result)
    assert str(result) == u'grid search\n# num_rows=3\n#   dim1,  dim2\n    0.10,  0.10\n    0.20,  0.40\n    0.30,  0.50'


def test_noexpand_parse_cfgstrs_0():
    import utool as ut
    cfgopt_strs = 'b=[1,2]'
    alias_keys = None
    cfg_combo = noexpand_parse_cfgstrs(cfgopt_strs, alias_keys)
    result = ('cfg_combo = %s' % (ut.repr2(cfg_combo, nl=0),))
    print(result)
    assert str(result) == u"cfg_combo = {'b': [1, 2]}"


def test_parse_cfgstr3_0():
    import utool as ut
    cfgopt_strs = 'b=[1,2]'
    cfgdict = parse_cfgstr3(cfgopt_strs)
    result = ('cfgdict = %s' % (ut.repr2(cfgdict),))
    print(result)
    assert str(result) == u"cfgdict = {'b': [1, 2]}"


def test_parse_cfgstr_list2_0():
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    cfgstr_list = ['name', 'name:f=1', 'name:b=[1,2]', 'name1:f=1::name2:f=1,b=2']
    #cfgstr_list = ['name', 'name1:f=1::name2:f=1,b=2']
    special_join_dict = {'joined': True}
    cfg_combos_list = parse_cfgstr_list2(
        cfgstr_list, named_defaults_dict, cfgtype, alias_keys, valid_keys,
        expand_nested, strict, special_join_dict)
    print('b' in cfg_combos_list[2][0])
    print('cfg_combos_list = %s' % (ut.list_str(cfg_combos_list, nl=2),))
    assert 'b' in cfg_combos_list[2][0], 'second cfg[2] should vary b'
    assert 'b' in cfg_combos_list[2][1], 'second cfg[2] should vary b'
    print(ut.depth_profile(cfg_combos_list))
    cfg_list = ut.flatten(cfg_combos_list)
    cfg_list = ut.flatten([cfg if isinstance(cfg, list) else [cfg] for cfg in cfg_list])
    result = ut.repr2(ut.get_varied_cfg_lbls(cfg_list))
    print(result)
    assert str(result) == u"['name:', 'name:f=1', 'name:b=1', 'name:b=2', 'name1:f=1,joined=True', 'name2:b=2,f=1,joined=True']"


def test_parse_cfgstr_list2_1():
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    # Allow for definition of a named default on the fly
    cfgstr_list = ['base=:f=2,c=[1,2]', 'base:f=1', 'base:b=[1,2]']
    special_join_dict = None
    cfg_combos_list = parse_cfgstr_list2(
        cfgstr_list, named_defaults_dict, cfgtype, alias_keys, valid_keys,
        expand_nested, strict, special_join_dict)
    print('cfg_combos_list = %s' % (ut.list_str(cfg_combos_list, nl=2),))
    print(ut.depth_profile(cfg_combos_list))
    cfg_list = ut.flatten(cfg_combos_list)
    cfg_list = ut.flatten([cfg if isinstance(cfg, list) else [cfg] for cfg in cfg_list])
    result = ut.repr2(ut.get_varied_cfg_lbls(cfg_list))
    print(result)
    assert str(result) == u"['base:c=1,f=1', 'base:c=2,f=1', 'base:b=1,c=1,f=2', 'base:b=1,c=2,f=2', 'base:b=2,c=1,f=2', 'base:b=2,c=2,f=2']"


def test_parse_cfgstr_list2_2():
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    cfgstr_list = ['base:f=2,c=[(1,2),(3,4)]']
    special_join_dict = None
    cfg_combos_list = parse_cfgstr_list2(
        cfgstr_list, named_defaults_dict, cfgtype, alias_keys, valid_keys,
        expand_nested, strict, special_join_dict)
    print('cfg_combos_list = %s' % (ut.list_str(cfg_combos_list, nl=2),))
    print(ut.depth_profile(cfg_combos_list))
    cfg_list = ut.flatten(cfg_combos_list)
    cfg_list = ut.flatten([cfg if isinstance(cfg, list) else [cfg] for cfg in cfg_list])
    result = ut.repr2(ut.get_varied_cfg_lbls(cfg_list))
    print(result)


def test_parse_cfgstr_list2_3():
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    import utool as ut
    named_defaults_dict = None
    cfgtype, alias_keys, valid_keys, metadata = None, None, None, None
    expand_nested, is_nestedcfgtypel, strict = True, False, False
    # test simplest case
    cfgstr_list = ['name:b=[1,2]']
    special_join_dict = {'joined': True}
    cfg_combos_list = parse_cfgstr_list2(
        cfgstr_list, named_defaults_dict, cfgtype, alias_keys, valid_keys,
        expand_nested, strict, special_join_dict)
    print('b' in cfg_combos_list[0][0])
    print('cfg_combos_list = %s' % (ut.list_str(cfg_combos_list, nl=2),))
    assert 'b' in cfg_combos_list[0][0], 'second cfg[2] should vary b'
    assert 'b' in cfg_combos_list[0][1], 'second cfg[2] should vary b'
    print(ut.depth_profile(cfg_combos_list))
    cfg_list = ut.flatten(cfg_combos_list)
    cfg_list = ut.flatten([cfg if isinstance(cfg, list) else [cfg] for cfg in cfg_list])
    result = ut.repr2(ut.get_varied_cfg_lbls(cfg_list))
    print(result)


def test_parse_cfgstr_name_options_0():
    import utool as ut
    cfgstr = 'default' + NAMEVARSEP + 'myvar1=myval1,myvar2=myval2'
    (cfgname, cfgopt_strs, subx) = parse_cfgstr_name_options(cfgstr)
    result = ('(cfgname, cfg_optstrs, subx) = %s' % (ut.repr2((cfgname, cfgopt_strs, subx)),))
    print(result)
    assert str(result) == u"(cfgname, cfg_optstrs, subx) = ('default', 'myvar1=myval1,myvar2=myval2', None)"


def test_parse_cfgstr_name_options_1():
    import utool as ut
    cfgstr = 'default[0:1]' + NAMEVARSEP + 'myvar1=myval1,myvar2=myval2'
    (cfgname, cfgopt_strs, subx) = parse_cfgstr_name_options(cfgstr)
    result = ('(cfgname, cfg_optstrs, subx) = %s' % (ut.repr2((cfgname, cfgopt_strs, subx)),))
    print(result)
    assert str(result) == u"(cfgname, cfg_optstrs, subx) = ('default', 'myvar1=myval1,myvar2=myval2', slice(0, 1, None))"


def test_parse_cfgstr_name_options_2():
    import utool as ut
    cfgstr = 'default[0]' + NAMEVARSEP + 'myvar1=myval1,myvar2=myval2'
    (cfgname, cfgopt_strs, subx) = parse_cfgstr_name_options(cfgstr)
    result = ('(cfgname, cfg_optstrs, subx) = %s' % (ut.repr2((cfgname, cfgopt_strs, subx)),))
    print(result)
    assert str(result) == u"(cfgname, cfg_optstrs, subx) = ('default', 'myvar1=myval1,myvar2=myval2', [0])"


def test_partition_varied_cfg_list_0():
    import utool as ut
    cfg_list = [{'f': 1, 'b': 1}, {'f': 2, 'b': 1}, {'f': 3, 'b': 1, 'z': 4}]
    nonvaried_cfg, varied_cfg_list = partition_varied_cfg_list(cfg_list)
    result = ut.list_str((nonvaried_cfg, varied_cfg_list), label_list=['nonvaried_cfg', 'varied_cfg_list'])
    print(result)
    assert str(result) == u"nonvaried_cfg = {'b': 1}\nvaried_cfg_list = [{'f': 1}, {'f': 2}, {'f': 3, 'z': 4}]"


def test_partition_varied_cfg_list_1():
    import utool as ut
    cfg_list = [{'q1': 1, 'f1': {'a2': {'x3': 1, 'y3': 2}, 'b2': 1}}, {'q1': 1, 'f1': {'a2': {'x3': 1, 'y3': 1}, 'b2': 1}, 'e1': 1}]
    print(ut.list_str(cfg_list, nl=True))
    nonvaried_cfg, varied_cfg_list = partition_varied_cfg_list(cfg_list, recursive=True)
    result = ut.list_str((nonvaried_cfg, varied_cfg_list), label_list=['nonvaried_cfg', 'varied_cfg_list'])
    print(result)
    assert str(result) == u"nonvaried_cfg = {'f1': {'a2': {'x3': 1}, 'b2': 1}, 'q1': 1}\nvaried_cfg_list = [{'f1': {'a2': {'y3': 2}}}, {'e1': 1, 'f1': {'a2': {'y3': 1}}}]"


def test_deterministic_shuffle_0():
    list_ = [1, 2, 3, 4, 5, 6]
    seed = 1
    list_ = deterministic_shuffle(list_, seed)
    result = str(list_)
    print(result)
    assert str(result) == u'[3, 2, 5, 1, 4, 6]'


def test_intersect2d_0():
    import utool as ut
    A = np.array([[1, 2, 3], [1, 1, 1]])
    B = np.array([[1, 2, 3], [1, 2, 14]])
    (C, Ax, Bx) = ut.intersect2d(A, B)
    result = str((C, Ax, Bx))
    print(result)
    assert str(result) == u'(array([[1, 2, 3]]), array([0]), array([0]))'


def test_sample_domain_0():
    import utool
    min_ = 10
    max_ = 1000
    nSamp  = 7
    result = utool.sample_domain(min_, max_, nSamp)
    assert str(result) == u'[10, 151, 293, 434, 576, 717, 859]'


def test_execstr_dict_1():
    import utool as ut
    my_dictionary = {'a': True, 'b': False}
    execstr = execstr_dict(my_dictionary)
    locals_ = locals()
    exec(execstr, locals_)
    a, b = ut.dict_take(locals_, ['a', 'b'])
    assert 'a' in locals_ and 'b' in locals_, 'execstr failed'
    assert b is False and a is True, 'execstr failed'
    result = execstr
    print(result)
    assert str(result) == u"a = my_dictionary['a']\nb = my_dictionary['b']"


def test_execstr_dict_2():
    import utool as ut
    my_dictionary = {'a': True, 'b': False}
    execstr = execstr_dict(my_dictionary, explicit=True)
    result = execstr
    print(result)
    assert str(result) == u'a = True\nb = False'


def test_get_caller_name_0():
    import utool as ut
    N = list(range(0, 13))
    allow_genexpr = True
    caller_name = get_caller_name(N, allow_genexpr)
    print(caller_name)


def test_parse_locals_keylist_0():
    import utool as ut
    locals_ = {'foo': [1, 2, 3], 'bar': 'spam', 'eggs': 4, 'num': 5}
    key_list = [(len, 'foo'), 'bar.lower.__name__', 'eggs', 'num', 'other']
    strlist_ = None
    prefix = u''
    strlist_ = parse_locals_keylist(locals_, key_list, strlist_, prefix)
    result = ('strlist_ = %s' % (ut.repr2(strlist_, nl=True),))
    print(result)
    assert str(result) == u'strlist_ = [\n    \' len(foo) = 3\',\n    " bar.lower.__name__ = \'lower\'",\n    \' eggs = 4\',\n    \' num = 5\',\n    \' other = NameError (this likely due to a misformatted printex and is not related to the exception)\',\n]'


def test_accepts_scalar_input_0():
    @accepts_scalar_input
    def foobar(self, list_):
        return [x + 1 for x in list_]
    self = None  # dummy self because this decorator is for classes
    assert 2 == foobar(self, 1)
    assert [2, 3] == foobar(self, [1, 2])


def test_memoize_0():
    import utool as ut
    closure = {'a': 'b', 'c': 'd'}
    incr = [0]
    def foo(key):
        value = closure[key]
        incr[0] += 1
        return value
    foo_memo = memoize(foo)
    assert foo('a') == 'b' and foo('c') == 'd'
    assert incr[0] == 2
    print('Call memoized version')
    assert foo_memo('a') == 'b' and foo_memo('c') == 'd'
    assert incr[0] == 4
    assert foo_memo('a') == 'b' and foo_memo('c') == 'd'
    print('Counter should no longer increase')
    assert incr[0] == 4
    print('Closure changes result without memoization')
    closure = {'a': 0, 'c': 1}
    assert foo('a') == 0 and foo('c') == 1
    assert incr[0] == 6
    assert foo_memo('a') == 'b' and foo_memo('c') == 'd'


def test_preserve_sig_0():
    import utool as ut
    #ut.rrrr(False)
    def myfunction(self, listinput_, arg1, *args, **kwargs):
        " just a test function "
        return [x + 1 for x in listinput_]
    #orig_func = ut.take
    orig_func = myfunction
    wrapper = ut.accepts_scalar_input2([0])(orig_func)
    _wrp_preserve1 = ut.preserve_sig(wrapper, orig_func, True)
    _wrp_preserve2 = ut.preserve_sig(wrapper, orig_func, False)
    print('_wrp_preserve2 = %r' % (_wrp_preserve1,))
    print('_wrp_preserve2 = %r' % (_wrp_preserve2,))
    print('source _wrp_preserve1 = %s' % (ut.get_func_sourcecode(_wrp_preserve1),))
    print('source _wrp_preserve2 = %s' % (ut.get_func_sourcecode(_wrp_preserve2)),)
    result = str(_wrp_preserve1)
    print(result)


def test_test_ignore_exec_traceback_0():
    result = test_ignore_exec_traceback()
    print(result)


def test_clean_dropbox_link_0():
    dropbox_url = 'www.dropbox.com/s/123456789abcdef/foobar.zip?dl=0'
    cleaned_url = clean_dropbox_link(dropbox_url)
    result = str(cleaned_url)
    print(result)
    assert str(result) == u'dl.dropbox.com/s/123456789abcdef/foobar.zip'


def test_grab_file_url_0():
    import utool as ut  # NOQA
    from os.path import basename
    file_url = 'http://i.imgur.com/JGrqMnV.png'
    ensure = True
    appname = 'utool'
    download_dir = None
    delay = None
    spoof = False
    verbose = True
    redownload = True
    fname = 'lena.png'
    lena_fpath = ut.grab_file_url(file_url, ensure, appname, download_dir,
                                  delay, spoof, fname, verbose, redownload)
    result = basename(lena_fpath)
    print(result)
    assert str(result) == u'lena.png'


def test_grab_test_imgpath_0():
    import utool as ut
    # build test data
    key = 'carl.jpg'
    # execute function
    testimg_fpath = grab_test_imgpath(key)
    # verify results
    ut.assertpath(testimg_fpath)


def test_cartesian_0():
    arrays = ([1, 2, 3], [4, 5], [6, 7])
    out = cartesian(arrays)
    result = repr(out.T)
    assert str(result) == u'array([[1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],\n       [4, 4, 5, 5, 4, 4, 5, 5, 4, 4, 5, 5],\n       [6, 7, 6, 7, 6, 7, 6, 7, 6, 7, 6, 7]])'


def test_ensure_crossplat_path_0():
    path = r'C:\somedir'
    cplat_path = ensure_crossplat_path(path)
    result = cplat_path
    print(result)
    assert str(result) == u'C:/somedir'


def test_get_modname_from_modpath_0():
    import utool as ut
    module_fpath = ut.util_path.__file__
    modname = ut.get_modname_from_modpath(module_fpath)
    result = modname
    print(result)
    assert str(result) == u'utool.util_path'


def test_get_modpath_0():
    import utool as ut
    utool_dir = dirname(dirname(ut.__file__))
    modname = 'utool.util_path'
    module_dir = get_modpath(modname)
    result = ut.truepath_relative(module_dir, utool_dir)
    result = ut.ensure_unixslash(result)
    print(result)
    assert str(result) == u'utool/util_path.py'


def test_get_modpath_1():
    import utool as ut
    utool_dir = dirname(dirname(ut.__file__))
    modname = 'utool._internal'
    module_dir = get_modpath(modname, prefer_pkg=True)
    result = ut.ensure_unixslash(module_dir)
    print(result)
    assert result.endswith('utool/_internal')


def test_get_modpath_2():
    import utool as ut
    utool_dir = dirname(dirname(ut.__file__))
    modname = 'utool'
    module_dir = get_modpath(modname)
    result = ut.truepath_relative(module_dir, utool_dir)
    result = ut.ensure_unixslash(result)
    print(result)
    assert str(result) == u'utool/__init__.py'


def test_get_module_subdir_list_0():
    import utool as ut
    module_fpath = ut.util_path.__file__
    modsubdir_list = get_module_subdir_list(module_fpath)
    result = modsubdir_list
    print(result)
    assert str(result) == u"['utool', 'util_path']"


def test_get_relative_modpath_0():
    import utool as ut
    module_fpath = ut.util_path.__file__
    rel_modpath = ut.get_relative_modpath(module_fpath)
    rel_modpath = rel_modpath.replace('.pyc', '.py')  # allow pyc or py
    result = ensure_crossplat_path(rel_modpath)
    print(result)
    assert str(result) == u'utool/util_path.py'


def test_glob_0():
    from os.path import dirname
    import utool as ut
    dpath = dirname(ut.__file__)
    pattern = '__*.py'
    recursive = True
    with_files = True
    with_dirs = True
    maxdepth = None
    fullpath = False
    exclude_dirs = ['_internal', join(dpath, 'experimental')]
    print('exclude_dirs = ' + ut.repr2(exclude_dirs))
    path_list = glob(dpath, pattern, recursive, with_files, with_dirs,
                     maxdepth, exclude_dirs, fullpath)
    path_list = sorted(path_list)
    result = ('path_list = %s' % (ut.repr3(path_list),))
    result = result.replace(r'\\', '/')
    print(result)
    assert str(result) == u"path_list = [\n    '__init__.py',\n    '__main__.py',\n    'tests/__init__.py',\n]"


def test_grep_0():
    import utool as ut
    #dpath_list = [ut.truepath('~/code/utool/utool')]
    dpath_list = [ut.truepath(dirname(ut.__file__))]
    include_patterns = ['*.py']
    exclude_dirs = []
    regex_list = ['grepfile']
    verbose = True
    recursive = True
    result = ut.grep(regex_list, recursive, dpath_list, include_patterns,
                     exclude_dirs)
    (found_fpath_list, found_lines_list, found_lxs_list) = result
    assert 'util_path.py' in list(map(basename, found_fpath_list))


def test_is_module_dir_0():
    path = truepath('~/code/utool/utool')
    flag = is_module_dir(path)
    result = (flag)
    print(result)


def test_longest_existing_path_0():
    import utool as ut
    target = dirname(ut.__file__)
    _path = join(target, 'nonexist/foobar')
    existing_path = longest_existing_path(_path)
    result = ('existing_path = %s' % (str(existing_path),))
    print(result)
    assert existing_path == target


def test_path_ndir_split_0():
    import utool as ut
    paths = [r'/usr/bin/local/foo/bar',
             r'C:/',
             #r'lonerel',
             #r'reldir/other',
             r'/ham',
             r'./eggs',
             r'/spam/eggs',
             r'C:\Program Files (x86)/foobar/bin']
    N = 2
    iter_ = ut.iprod(paths, range(1, N + 1))
    force_unix = True
    tuplist = [(n, path_ndir_split(path_, n)) for path_, n in iter_]
    chunklist = list(ut.ichunks(tuplist, N))
    list_ = [['n=%r: %s' % (x, ut.reprfunc(y)) for x, y in chunk]
             for chunk in chunklist]
    line_list = [', '.join(strs) for strs in list_]
    result = '\n'.join(line_list)
    print(result)
    assert str(result) == u"n=1: '.../bar', n=2: '.../foo/bar'\nn=1: 'C:/', n=2: 'C:/'\nn=1: '.../ham', n=2: '/ham'\nn=1: '.../eggs', n=2: './eggs'\nn=1: '.../eggs', n=2: '.../spam/eggs'\nn=1: '.../bin', n=2: '.../foobar/bin'"


def test_platform_path_0():
    # FIXME: find examples of the wird paths this fixes (mostly on win32 i think)
    import utool as ut
    path = 'some/odd/../weird/path'
    path2 = platform_path(path)
    result = str(path2)
    if ut.WIN32:
        ut.assert_eq(path2, r'some\weird\path')
    else:
        ut.assert_eq(path2, r'some/weird/path')


def test_platform_path_1():
    import utool as ut    # NOQA
    if ut.WIN32:
        path = 'C:/PROGRA~2'
        path2 = platform_path(path)
        assert path2 == u'..\\..\\..\\..\\Program Files (x86)'


def test_remove_broken_links_1():
    import utool as ut
    dpath = ut.ensure_app_resource_dir('utool', 'path_tests')
    ut.delete(dpath)
    test_dpath = ut.ensuredir(join(dpath, 'testdpath'))
    test_fpath = ut.ensurefile(join(dpath, 'testfpath.txt'))
    flink1 = ut.symlink(test_fpath, join(dpath, 'flink1'))
    dlink1 = ut.symlink(test_fpath, join(dpath, 'dlink1'))
    assert len(ut.ls(dpath)) == 4
    ut.delete(test_fpath)
    assert len(ut.ls(dpath)) == 3
    remove_broken_links(dpath)
    ut.delete(test_dpath)
    remove_broken_links(dpath)
    assert len(ut.ls(dpath)) == 0


def test_remove_dirs_0():
    import utool as ut
    dpath = ut.ensure_app_resource_dir('utool', 'testremovedir')
    assert exists(dpath), 'nothing to remove'
    dryrun = False
    ignore_errors = True
    quiet = False
    flag = remove_dirs(dpath, dryrun, ignore_errors, quiet)
    result = ('flag = %s' % (flag,))
    print(result)
    assert not exists(dpath), 'did not remove dpath'
    assert str(result) == u'flag = True'


def test_sedfile_0():
    import utool as ut
    fpath = ut.get_modpath(ut.util_path)
    regexpr = 'sedfile'
    repl = 'saidfile'
    force = False
    verbose = True
    veryverbose = False
    changed_lines = sedfile(fpath, regexpr, repl, force, verbose, veryverbose)
    result = ('changed_lines = %s' % (ut.repr3(changed_lines),))
    print(result)


def test_testgrep_0():
    import utool as ut
    #dpath_list = [ut.truepath('~/code/utool/utool')]
    dpath_list = [ut.truepath(dirname(ut.__file__))]
    include_patterns = ['*.py']
    exclude_dirs = []
    regex_list = ['grepfile']
    verbose = True
    recursive = True
    result = ut.grep(regex_list, recursive, dpath_list, include_patterns,
                     exclude_dirs)
    (found_fpath_list, found_lines_list, found_lxs_list) = result
    assert 'util_path.py' in list(map(basename, found_fpath_list))


def test_truepath_relative_0():
    import utool as ut
    path = 'C:/foobar/foobiz'
    otherpath = 'C:/foobar'
    path_ = truepath_relative(path, otherpath)
    result = ('path_ = %s' % (ut.repr2(path_),))
    print(result)
    assert str(result) == u"path_ = 'foobiz'"


def test_named_field_regex_0():
    keypat_tups = [
        ('name',  r'G\d+'),  # species and 2 numbers
        ('under', r'_'),     # 2 more numbers
        ('id',    r'\d+'),   # 2 more numbers
        ( None,   r'\.'),
        ('ext',   r'\w+'),
    ]
    regex = named_field_regex(keypat_tups)
    result = (regex)
    print(result)
    assert str(result) == u'(?P<name>G\\d+)(?P<under>_)(?P<id>\\d+)(\\.)(?P<ext>\\w+)'


def test_named_field_repl_0():
    field_list = [('key',), 'unspecial string']
    repl = named_field_repl(field_list)
    result = repl
    print(result)
    assert str(result) == u'\\g<key>unspecial string'


def test_regex_replace_0():
    regex = r'\(.*\):'
    repl = '(*args)'
    text = '''def foo(param1,
                      param2,
                      param3):'''
    result = regex_replace(regex, repl, text)
    print(result)
    assert str(result) == u'def foo(*args)'


def test_regex_replace_1():
    import utool as ut
    regex = ut.named_field_regex([('keyword', 'def'), ' ', ('funcname', '.*'), '\(.*\):'])
    repl = ut.named_field_repl([('funcname',), ('keyword',)])
    text = '''def foo(param1,
                      param2,
                      param3):'''
    result = regex_replace(regex, repl, text)
    print(result)
    assert str(result) == u'foodef'


def test_get_doctest_examples_0():
    func_or_class = get_doctest_examples
    tup  = get_doctest_examples(func_or_class)
    testsrc_list, testwant_list, testlinenum_list, func_lineno, docstr = tup
    result = str(len(testsrc_list) + len(testwant_list))
    print(testsrc_list)
    print(testlinenum_list)
    print(func_lineno)
    print(testwant_list)
    print(result)
    assert str(result) == u'6'


def test_get_doctest_examples_1():
    import utool as ut
    func_or_class = ut.tryimport
    tup = get_doctest_examples(func_or_class)
    testsrc_list, testwant_list, testlinenum_list, func_lineno, docstr = tup
    result = str(len(testsrc_list) + len(testwant_list))
    print(testsrc_list)
    print(testlinenum_list)
    print(func_lineno)
    print(testwant_list)
    print(result)
    assert str(result) == u'4'


def test_get_module_doctest_tup_0():
    import utool as ut
    #testable_list = [ut.util_import.package_contents]
    testable_list = None
    check_flags = False
    module = ut.util_cplat
    allexamples = False
    needs_enable = None
    N = 0
    verbose = True
    testslow = False
    mod_doctest_tup = get_module_doctest_tup(testable_list, check_flags, module, allexamples, needs_enable, N, verbose, testslow)
    result = ('mod_doctest_tup = %s' % (ut.list_str(mod_doctest_tup, nl=4),))
    print(result)


def test_parse_docblocks_from_docstr_0():
    import utool as ut
    func_or_class = ut.parse_docblocks_from_docstr
    docstr = ut.get_docstr(func_or_class)
    docstr_blocks = parse_docblocks_from_docstr(docstr)
    result = str(docstr_blocks)
    print(result)


def test_parse_doctest_from_docstr_0():
    import utool as ut
    #from ibeis.algo.hots import score_normalization
    #func_or_class = score_normalization.cached_ibeis_score_normalizer
    func_or_class = parse_doctest_from_docstr
    docstr = ut.get_docstr(func_or_class)
    testsrc_list, testwant_list, testlinenum_list, func_lineno, docstr = get_doctest_examples(func_or_class)
    print('\n\n'.join(testsrc_list))
    assert len(testsrc_list) == len(testwant_list)


def test_make_args_docstr_0():
    argname_list = ['argname_list', 'argtype_list', 'argdesc_list']
    argtype_list = ['list', 'list', 'list']
    argdesc_list = ['names', 'types', 'descriptions']
    ismethod = False
    arg_docstr = make_args_docstr(argname_list, argtype_list, argdesc_list, ismethod)
    result = str(arg_docstr)
    print(result)
    assert str(result) == u'argname_list (list): names\nargtype_list (list): types\nargdesc_list (list): descriptions'


def test_make_default_docstr_0():
    import utool as ut
    func = ut.make_default_docstr
    #func = ut.make_args_docstr
    func = PythonStatement
    default_docstr = make_default_docstr(func)
    result = str(default_docstr)
    print(result)


def test_make_default_module_maintest_0():
    modname = 'utool.util_autogen'
    text = make_default_module_maintest(modname)
    result = str(text)
    print(result)


def test_make_example_docstr_0():
    # build test data
    funcname = 'make_example_docstr'
    modname = 'utool.util_autogen'
    argname_list = ['qaids', 'qreq_']
    defaults = None
    return_type = tuple
    return_name = 'foo'
    ismethod = False
    # execute function
    examplecode = make_example_docstr(funcname, modname, argname_list, defaults, return_type, return_name, ismethod)
    # verify results
    result = str(examplecode)
    print(result)
    assert str(result) == u"# DISABLE_DOCTEST\nfrom utool.util_autogen import *  # NOQA\nimport utool as ut\nimport ibeis\nspecies = ibeis.const.TEST_SPECIES.ZEB_PLAIN\nqaids = ibs.get_valid_aids(species=species)\nqreq_ = ibeis.testdata_qreq_()\nfoo = make_example_docstr(qaids, qreq_)\nresult = ('foo = %s' % (ut.repr2(foo),))\nprint(result)"


def test_hashable_to_uuid_0():
    hashable_ = 'foobar'
    uuid_ = hashable_to_uuid(hashable_)
    result = str(uuid_)
    print(result)
    assert str(result) == u'8843d7f9-2416-211d-e9eb-b963ff4ce281'


def test_hashable_to_uuid_1():
    hashable_ = u'foobar'
    uuid_ = hashable_to_uuid(hashable_)
    result = str(uuid_)
    print(result)
    assert str(result) == u'8843d7f9-2416-211d-e9eb-b963ff4ce281'


def test_hashable_to_uuid_2():
    hashable_ = 10
    uuid_ = hashable_to_uuid(hashable_)
    result = str(uuid_)
    print(result)
    assert str(result) == u'b1d57811-11d8-4f7b-3fe4-5a0852e59758'


def test_hashstr_0():
    data = 'foobar'
    hashlen = 16
    alphabet = ALPHABET
    text = hashstr(data, hashlen, alphabet)
    result = ('text = %s' % (str(text),))
    print(result)
    assert str(result) == u'text = mi5yum60mbxhyp+x'


def test_hashstr_1():
    data = ''
    hashlen = 16
    alphabet = ALPHABET
    text = hashstr(data, hashlen, alphabet)
    result = ('text = %s' % (str(text),))
    print(result)
    assert str(result) == u'text = 0000000000000000'


def test_hashstr_2():
    import numpy as np
    data = np.array([1, 2, 3])
    hashlen = 16
    alphabet = ALPHABET
    text = hashstr(data, hashlen, alphabet)
    result = ('text = %s' % (str(text),))
    print(result)
    assert str(result) == u'text = z5lqw0bzt4dmb9yy'


def test_hashstr_arr_0():
    import numpy as np
    arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    lbl = 'arr'
    kwargs = {}
    pathsafe = False
    arr_hashstr = hashstr_arr(arr, lbl, pathsafe, alphabet=ALPHABET_27)
    result = ('arr_hashstr = %s' % (str(arr_hashstr),))
    print(result)
    assert str(result) == u'arr_hashstr = arr((2,3)daukyreqnhfejkfs)'


def test_hashstr_arr_1():
    import numpy as np
    arr = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
    kwargs = {}
    lbl = 'arr'
    pathsafe = True
    arr_hashstr = hashstr_arr(arr, lbl, pathsafe, alphabet=ALPHABET_27)
    result = ('arr_hashstr = %s' % (str(arr_hashstr),))
    print(result)
    assert str(result) == u'arr_hashstr = arr-_2,3_daukyreqnhfejkfs-'


def test_apply_grouping_0():
    import utool as ut
    idx2_groupid = [2, 1, 2, 1, 2, 1, 2, 3, 3, 3, 3]
    items        = [1, 8, 5, 5, 8, 6, 7, 5, 3, 0, 9]
    (keys, groupxs) = ut.group_indices(idx2_groupid)
    grouped_items = ut.apply_grouping(items, groupxs)
    result = ut.repr2(grouped_items)
    print(result)
    assert str(result) == u'[[8, 5, 6], [1, 5, 8, 7], [5, 3, 0, 9]]'


def test_bayes_rule_0():
    b_given_a = .1
    prob_a = .3
    prob_b = .4
    a_given_b = bayes_rule(b_given_a, prob_a, prob_b)
    result = a_given_b
    print(result)
    assert str(result) == u'0.075'


def test_compare_groupings_0():
    groups1 = [[1, 2, 3], [4], [5, 6], [7, 8], [9, 10, 11]]
    groups2 = [[1, 2, 11], [3, 4], [5, 6], [7], [8, 9], [10]]
    total_error = compare_groupings(groups1, groups2)
    result = ('total_error = %r' % (total_error,))
    print(result)
    assert str(result) == u'total_error = 20'


def test_compare_groupings_1():
    groups1 = [[1, 2, 3], [4], [5, 6]]
    groups2 = [[1, 2, 3], [4], [5, 6]]
    total_error = compare_groupings(groups1, groups2)
    result = ('total_error = %r' % (total_error,))
    print(result)
    assert str(result) == u'total_error = 0'


def test_compare_groupings_2():
    groups1 = [[1, 2, 3], [4], [5, 6]]
    groups2 = [[1, 2], [4], [5, 6]]
    total_error = compare_groupings(groups1, groups2)
    result = ('total_error = %r' % (total_error,))
    print(result)
    assert str(result) == u'total_error = 4'


def test_cumsum_0():
    import utool as ut
    item_list = [1, 2, 3, 4, 5]
    initial = 0
    result = cumsum(item_list, initial)
    assert result == [1, 3, 6, 10, 15]
    print(result)
    item_list = zip([1, 2, 3, 4, 5])
    initial = tuple()
    result2 = cumsum(item_list, initial)
    assert result2 == [(1,), (1, 2), (1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5)]
    print(result2)


def test_diagonalized_iter_0():
    import utool as ut
    size = ut.get_argval('--size', default=4)
    iter_ = diagonalized_iter(size)
    mat = [[None] * size for _ in range(size)]
    for count, (r, c) in enumerate(iter_):
        mat[r][c] = count
    result = ut.repr2(mat, nl=1, packed=True)
    print(result)
    assert str(result) == u'[[0, 2, 5, 9],\n [1, 4, 8, 12],\n [3, 7, 11, 14],\n [6, 10, 13, 15],]'


def test_fibonacci_iterative_0():
    import utool as ut
    with ut.Timer('fib iter'):
        series = [fibonacci_iterative(n) for n in range(20)]
    result = ('series = %s' % (str(series[0:10]),))
    print(result)
    assert str(result) == u'series = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]'


def test_fibonacci_recursive_0():
    import utool as ut
    with ut.Timer('fib rec'):
        series = [fibonacci_recursive(n) for n in range(20)]
    result = ('series = %s' % (str(series[0:10]),))
    print(result)
    assert str(result) == u'series = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]'


def test_find_grouping_consistencies_0():
    groups1 = [[1, 2, 3], [4], [5, 6]]
    groups2 = [[1, 2], [4], [5, 6]]
    common_groups = find_grouping_consistencies(groups1, groups2)
    result = ('common_groups = %r' % (common_groups,))
    print(result)
    assert str(result) == u'common_groups = [(5, 6), (4,)]'


def test_greedy_max_inden_setcover_0():
    import utool as ut
    candidate_sets_dict = {'a': [5, 3], 'b': [2, 3, 5],
                           'c': [4, 8], 'd': [7, 6, 2, 1]}
    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    max_covers = None
    tup = greedy_max_inden_setcover(candidate_sets_dict, items, max_covers)
    (uncovered_items, covered_items_list, accepted_keys) = tup
    result = ut.list_str((uncovered_items, sorted(list(accepted_keys))), nl=False)
    print(result)
    assert str(result) == u"([0, 9], ['a', 'c', 'd'])"


def test_greedy_max_inden_setcover_1():
    import utool as ut
    candidate_sets_dict = {'a': [5, 3], 'b': [2, 3, 5],
                           'c': [4, 8], 'd': [7, 6, 2, 1]}
    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    max_covers = 1
    tup = greedy_max_inden_setcover(candidate_sets_dict, items, max_covers)
    (uncovered_items, covered_items_list, accepted_keys) = tup
    result = ut.list_str((uncovered_items, sorted(list(accepted_keys))), nl=False)
    print(result)
    assert str(result) == u"([0, 3, 4, 5, 8, 9], ['d'])"


def test_group_indices_0():
    import utool as ut
    groupid_list = ['b', 1, 'b', 1, 'b', 1, 'b', 'c', 'c', 'c', 'c']
    (keys, groupxs) = ut.group_indices(groupid_list)
    result = ut.repr3((keys, groupxs), nobraces=1, nl=1)
    print(result)
    assert str(result) == u"[1, 'b', 'c'],\n[[1, 3, 5], [0, 2, 4, 6], [7, 8, 9, 10]],"


def test_is_prime_0():
    import utool as ut
    with ut.Timer('isprime'):
        series = [is_prime(n) for n in range(30)]
    result = ('primes = %s' % (str(ut.list_where(series[0:10])),))
    print(result)
    assert str(result) == u'primes = [2, 3, 5, 7]'


def test_knapsack_0():
    import utool as ut
    items = [(4, 12, 0), (2, 1, 1), (6, 4, 2), (1, 1, 3), (2, 2, 4)]
    maxweight = 15
    total_value, items_subset = knapsack(items, maxweight, method='recursive')
    total_value1, items_subset1 = knapsack(items, maxweight, method='iterative')
    result =  'total_value = %.2f\n' % (total_value,)
    result += 'items_subset = %r' % (items_subset,)
    print(result)
    ut.assert_eq(total_value1, total_value)
    ut.assert_eq(items_subset1, items_subset)
    assert str(result) == u'total_value = 11.00\nitems_subset = [(2, 1, 1), (6, 4, 2), (1, 1, 3), (2, 2, 4)]'


def test_knapsack_1():
    import utool as ut
    # Solve https://xkcd.com/287/
    weights = [2.15, 2.75, 3.35, 3.55, 4.2, 5.8] * 2
    items = [(w, w, i) for i, w in enumerate(weights)]
    maxweight = 15.05
    total_value, items_subset = knapsack(items, maxweight, method='recursive')
    total_value1, items_subset1 = knapsack(items, maxweight, method='iterative')
    total_weight = sum([t[1] for t in items_subset])
    print('total_weight = %r' % (total_weight,))
    result =  'total_value = %.2f' % (total_value,)
    print(result)
    print('items_subset = %r' % (items_subset,))
    print('items_subset1 = %r' % (items_subset1,))
    #assert items_subset1 == items_subset, 'NOT EQ\n%r !=\n%r' % (items_subset1, items_subset)
    assert str(result) == u'total_value = 15.05'


def test_knapsack_greedy_0():
    items = [(4, 12, 0), (2, 1, 1), (6, 4, 2), (1, 1, 3), (2, 2, 4)]
    maxweight = 15
    total_value, items_subset = knapsack_greedy(items, maxweight)
    result =  'total_value = %r\n' % (total_value,)
    result += 'items_subset = %r' % (items_subset,)
    print(result)
    assert str(result) == u'total_value = 7\nitems_subset = [(4, 12, 0), (2, 1, 1), (1, 1, 3)]'


def test_knapsack_iterative_int_0():
    weights = [1, 3, 3, 5, 2, 1] * 2
    items = [(w, w, i) for i, w in enumerate(weights)]
    maxweight = 10
    items = [(.8, 700, 0)]
    maxweight = 2000
    print('maxweight = %r' % (maxweight,))
    print('items = %r' % (items,))
    total_value, items_subset = knapsack_iterative_int(items, maxweight)
    total_weight = sum([t[1] for t in items_subset])
    print('total_weight = %r' % (total_weight,))
    print('items_subset = %r' % (items_subset,))
    result =  'total_value = %.2f' % (total_value,)
    print(result)
    assert str(result) == u'total_value = 0.80'


def test_norm_zero_one_0():
    array = np.array([ 22, 1, 3, 2, 10, 42, ])
    dim = None
    array_norm = norm_zero_one(array, dim)
    result = np.array_str(array_norm, precision=3)
    print(result)
    assert str(result) == u'[ 0.512  0.     0.049  0.024  0.22   1.   ]'


def test_number_of_decimals_0():
    num = 15.05
    result = number_of_decimals(num)
    print(result)
    assert str(result) == u'2'


def test_ungroup_0():
    import utool as ut
    grouped_items = [[1.1, 1.2], [2.1, 2.2], [3.1, 3.2]]
    groupxs = [[0, 2], [1, 5], [4, 3]]
    maxval = None
    ungrouped_items = ungroup(grouped_items, groupxs, maxval)
    result = ('ungrouped_items = %s' % (ut.repr2(ungrouped_items),))
    print(result)
    assert str(result) == u'ungrouped_items = [1.1, 2.1, 1.2, 3.2, 3.1, 2.2]'


def test_ungroup_gen_0():
    import utool as ut
    grouped_items = [[1.1, 1.2], [2.1, 2.2], [3.1, 3.2]]
    groupxs = [[1, 2], [5, 6], [9, 3]]
    ungrouped_items1 = list(ungroup_gen(grouped_items, groupxs))
    ungrouped_items2 = ungroup(grouped_items, groupxs)
    assert ungrouped_items1 == ungrouped_items2
    grouped_items = [[1.1, 1.2], [2.1, 2.2], [3.1, 3.2]]
    groupxs = [[0, 2], [1, 5], [4, 3]]
    ungrouped_items1 = list(ungroup_gen(grouped_items, groupxs))
    ungrouped_items2 = ungroup(grouped_items, groupxs)
    assert ungrouped_items1 == ungrouped_items2


def test_ungroup_unique_0():
    import utool as ut
    unique_items = [1, 2, 3]
    groupxs = [[0, 2], [1, 3], [4, 5]]
    maxval = None
    ungrouped_items = ungroup_unique(unique_items, groupxs, maxval)
    result = ('ungrouped_items = %s' % (ut.repr2(ungrouped_items),))
    print(result)
    assert str(result) == u'ungrouped_items = [1, 2, 1, 2, 3, 3]'


def test_upper_diag_self_prodx_0():
    list_ = [1, 2, 3]
    result = upper_diag_self_prodx(list_)
    print(result)
    assert str(result) == u'[(1, 2), (1, 3), (2, 3)]'


def test_get_python_datastructure_sizes_0():
    import utool as ut  # NOQA
    type_sizes = get_python_datastructure_sizes()
    result = ut.dict_str(type_sizes, sorted_=True)
    print(result)
