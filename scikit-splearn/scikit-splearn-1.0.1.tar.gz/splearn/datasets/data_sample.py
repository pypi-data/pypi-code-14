# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
#
# Copyright(c) 2016
# -----------------
#
# * LabEx Archimède: http://labex-archimede.univ-amu.fr/
# * Laboratoire d'Informatique Fondamentale : http://www.lif.univ-mrs.fr/
#
# Contributors:
# ------------
#
# * François Denis <francois.denis_AT_lif.univ-mrs.fr>
# * Rémy Eyraud <remy.eyraud_AT_lif.univ-mrs.fr>
# * Denis Arrivault <contact.dev_AT_lif.univ-mrs.fr>
# * Dominique Benielli <dominique.benielli_AT_univ-amu.fr>
#
# Description:
# -----------
#
# scitkit-splearn is a toolbox in
# python for spectral learning algorithms.
#
# Version:
# -------
#
# * splearn version = 1.0.1
#
# Licence:
# -------
#
# License: 3-clause BSD
#
#
# ######### COPYRIGHT #########
"""This module contains the DataSample class and Splearn_array class
The DataSample class encapsulates a sample 's components
nbL and nbEx numbers,
Splearn_array class inherit from numpy ndarray and contains a 2d data ndarray
with the shape

==== ====  ====  ====  ====
x    x     x     x     -1
x    x     x     x     x
x    x     -1    -1    -1
x    -1    -1    -1    -1
-1   -1    -1    -1    -1
==== ====  ====  ====  ====

where -1 a indicates a empty cell,
the number nbL and nbEx and , the fourth dictionaries for sample,
prefix, suffix and factor where they are computed
"""
import numpy as np


class Splearn_array(np.ndarray):
    """Splearn_array inherit from numpy ndarray

    :Example:

    >>> from splearn.datasets.base import load_data_sample
    >>> from splearn.tests.datasets.get_dataset_path import get_dataset_path
    >>> train_file = '3.pautomac_light.train' # '4.spice.train'
    >>> data = load_data_sample(adr=get_dataset_path(train_file))
    >>> print(data.__class__)
    >>> data.data
    <class 'splearn.datasets.data_sample.DataSample'>
    GSplearn_array([[ 3.,  0.,  3., ..., -1., -1., -1.],
        [ 3.,  3., -1., ..., -1., -1., -1.],
        [ 3.,  2.,  0., ..., -1., -1., -1.],
        ...,
        [ 3.,  1.,  3., ..., -1., -1., -1.],
        [ 3.,  0.,  3., ..., -1., -1., -1.],
        [ 3.,  3.,  1., ..., -1., -1., -1.]])
    """
    def __new__(cls, input_array, nbL=None, nbEx=None,
                sample=None, pref=None,
                suff=None, fact=None, *args, **kwargs):
        obj = np.asarray(input_array).view(cls)
        obj.nbL = nbL
        obj.nbEx = nbEx
        obj.sample = sample
        obj.pref = pref
        obj.suff = suff
        obj.fact = fact
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.nbL = getattr(obj, 'nbL', None)
        self.nbEx = getattr(obj, 'nbEx', None)

        self.sample = getattr(obj, 'sample', None)
        self.pref = getattr(obj, 'pref', None)
        self.suff = getattr(obj, 'suff', None)
        self.fact = getattr(obj, 'fact', None)

    # def select_rows(self, nb_rows_max=1000, version='classic'):
    #     """define lrows
    #
    #     - Input:
    #
    #     :param int nb_rows_max:  (default = 1000) number of maximum rows
    #     :param string version: (default = "classic") version name
    #
    #     - Output:
    #
    #     :returns: list lrows,  list of rows
    #     :rtype: list
    #     """
    #     lRows = []  # liste à renvoyer
    #     nbRows = 0
    #     lLeafs = [([], self.nbEx )]
    #     #  pref[()]la liste de couples (prefixes frontières, nb occ)
    #     # initialisée au prefixe vide
    #     if version == 'classic':
    #         while lLeafs and nbRows < nb_rows_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le prefixe frontière le plus fréquent
    #             lRows.append(tuple(lastWord))
    #             nbRows += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.pref:
    #                     # ajout d'un nouveau prefixe frontière
    #                     lLeafs.append((newWord, self.pref[tnewWord]))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[1])
    #     elif version == 'prefix':
    #         while lLeafs and nbRows < nb_rows_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le prefixe frontière le plus fréquent
    #             lRows.append(tuple(lastWord))
    #             nbRows += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.pref:
    #                     # ajout d'un nouveau prefixe frontière
    #                     nb = 0
    #                     for u in self.sample:
    #                         if tnewWord <= u:
    #                             nb += self.sample[u] * (
    #                             len(u) - len(tnewWord) + 1)
    #                     lLeafs.append((newWord, nb))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[1])
    #     elif version == 'factor':
    #         while lLeafs and nbRows < nb_rows_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le prefixe frontière le plus fréquent
    #             lRows.append(tuple(lastWord))
    #             nbRows += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.fact:
    #                     # ajout d'un nouveau prefixe frontière
    #                     nb = 0
    #                     lw = len(tnewWord)
    #                     for u in self.sample:
    #                         if len(u) >= lw:
    #                             for i in range(lw, len(u) + 1):
    #                                 if u[:i][-lw:] == tnewWord:
    #                                     nb += self.sample[u] * (len(u) - i + 1)
    #                     lLeafs.append((newWord, nb))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[1])
    #             # print(lLeafs)
    #     return lRows

    # def select_columns(self, nb_columns_max=1000, version='classic'):
    #     """define lcolumns
    #
    #     - Input:
    #
    #     :param int nb_columns_max:  (default = 1000) number of maximum columns
    #     :param string version: (default = "classic") version name
    #
    #     - Output:
    #
    #     :returns:list lcolumns,  list of columns
    #     :rtype: list
    #     """
    #     lColumns = []  # liste à renvoyer
    #     lLeafs = [([], self.nbEx)]  # la liste de couples (suffixes frontières,
    #     #  nb occ) initialisée au suffixe vide
    #
    #     nbColumns = 0
    #     if version == 'classic':
    #          while lLeafs and nbColumns < nb_columns_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le suffixe frontière le plus fréquent
    #             lColumns.append(tuple(lastWord))
    #             nbColumns += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.suff:
    #                     # ajout d'un nouveau suffixe frontière
    #                     lLeafs.append((newWord, self.suff[tnewWord]))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[
    #                 1])  # suffixe le plus fréquent en dernier
    #             # print(lLeafs)
    #     elif version == 'prefix':
    #         while lLeafs and nbColumns < nb_columns_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le prefixe frontière le plus fréquent
    #             lColumns.append(tuple(lastWord))
    #             nbColumns += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.fact:
    #                     # ajout d'un nouveau suffixe frontière
    #                     lLeafs.append((newWord, self.fact[tnewWord]))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[1])
    #     elif version == 'factor':
    #         while lLeafs and nbColumns < nb_columns_max:
    #             lastWord = lLeafs.pop()[
    #                 0]  # le prefixe frontière le plus fréquent
    #             lColumns.append(tuple(lastWord))
    #             nbColumns += 1
    #             for i in range(self.nbL):
    #                 newWord = lastWord + [i]  # successeur de lastword
    #                 tnewWord = tuple(newWord)  # tuple associé
    #                 if tnewWord in self.fact:
    #                     # ajout d'un nouveau prefixe frontière
    #                     nb = 0
    #                     lw = len(tnewWord)
    #                     for u in self.sample:
    #                         if len(u) >= lw:
    #                             for i in range(lw, len(u) + 1):
    #                                 if u[:i][-lw:] == tnewWord:
    #                                     nb += self.sample[u] * (i - lw + 1)
    #                     lLeafs.append((newWord, nb))
    #             lLeafs = sorted(lLeafs, key=lambda x: x[1])
    #             # print(lLeafs)
    #     return lColumns

class DataSample(dict):
    """ A DataSample instance

    :Example:

    >>> from splearn.datasets.base import load_data_sample
    >>> from splearn.tests.datasets.get_dataset_path import get_dataset_path
    >>> train_file = '3.pautomac_light.train' # '4.spice.train'
    >>> data = load_data_sample(adr=get_dataset_path(train_file))
    >>> print(data.__class__)
    <class 'splearn.datasets.data_sample.DataSample'>
    >>> data.nbL
    4
    >>> data.nbEx
    5000
    >>> data.data

    - Input:

    :param string adr: adresse and name of the loaden file
    :param string type: (default value = 'SPiCe') indicate
           the structure of the file
    :param lrows: number or list of rows,
           a list of strings if partial=True;
           otherwise, based on self.pref if version="classic" or
           "prefix", self.fact otherwise
    :type lrows: int or list of int
    :param lcolumns: number or list of columns
           a list of strings if partial=True ;
           otherwise, based on self.suff if version="classic" or "suffix",
           self.fact otherwise
    :type lcolumns: int or list of int
    :param string version: (default = "classic") version name
    :param boolean partial: (default value = False) build of partial

    """

    def __init__(self, data=None, type='SPiCe', **kwargs):

        # Size of the alphabet
        self._nbL = 0
        # Number of samples
        self._nbEx = 0
        # The dictionary that contains the sample
        self._data = Splearn_array(np.zeros((0,0)))
        if data is not None:
            self.nbL = data[0]
            self.nbEx = data[1]
            self.data = Splearn_array(data[2], nbL=data[0], nbEx=data[1])

        super(DataSample, self).__init__(kwargs)


    @property
    def nbL(self):
        """Number of letters"""
        return self._nbL

    @nbL.setter
    def nbL(self, nbL):
        if not isinstance(nbL, int):
            raise TypeError("nbL should be an integer")
        if nbL < 0:
            raise ValueError("The size of the alphabet should " +
                             "an integer >= 0")
        self._nbL = nbL

    @property
    def nbEx(self):
        """Number of examples"""

        return self._nbEx

    @nbEx.setter
    def nbEx(self, nbEx):
        if not isinstance(nbEx, int):
            raise TypeError("nbEx should be an integer")
        if nbEx < 0:
            raise ValueError("The number of examples should be " +
                             " an integer >= 0")
        self._nbEx = nbEx

    @property
    def data(self):
        """Splearn_array"""

        return self._data

    @data.setter
    def data(self, data):
        if isinstance(data, (Splearn_array, np.ndarray, np.generic)):
            self._data = data
        else:
            raise TypeError("sample should be a Splearn_array.")




