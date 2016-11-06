#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages

setup(name='BitVector',
      version='3.4.5',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/dist/BitVector-3.4.5.html',
      download_url='https://engineering.purdue.edu/kak/dist/BitVector-3.4.5.tar.gz#md5=832b368cd8e4928a1f3b1aa58ac80aa6',
      description='A memory-efficient packed representation for bit arrays in pure Python',
      long_description='''
This class presents a memory-efficient packed representation for bit arrays in pure Python and the code for using the representation in applications such as computer security, computer vision, etc.

**Version 3.4.5** fixes an important bug in the slice assignment code. The bug made itself evident when using negative start/stop values for slice assignment.  This version also include a new method named min_canonical() that returns a canonical form of a bit pattern, which is a circularly shifted form of a bit pattern that has the maximum number of leading zeros.  This method is useful in the "Local Binary Pattern" algorithm for characterizing image textures.

The class is provided with the following operators/methods:

-      __getitem__
-      __setitem__
-      __len__
-      __iter__
-      __contains__
-      __str__
-      __int__
-      __add__
-      __eq__, __ne__, __lt__, __le__, __gt__, __ge__
-      __or__
-      __and__
-      __xor__
-      __invert__
-      __lshift__
-      __rshift__
-      __add__
-      close_file_object
-      count_bits 
-      count_bits_sparse      (faster for sparse bit vectors)     
-      deep_copy
-      divide_into_two
-      gcd                    (for greatest common divisor)
-      gen_random_bits 
-      get_bitvector_in_ascii
-      get_bitvector_in_hex
-      gf_divide_by_modulus   (for modular divisions in GF(2^n))
-      gf_MI                  (for multiplicative inverse in GF(2^n))
-      gf_multiply            (for multiplications in GF(2))
-      gf_multiply_modular    (for multiplications in GF(2^n))
-      hamming_distance
-      int_val                (for returning the integer value) 
-      is_power_of_2
-      is_power_of_2_sparse   (faster for sparse bit vectors)
-      jaccard_distance
-      jaccard_similarity
-      length                 
-      min_canonical
-      multiplicative_inverse
-      next_set_bit
-      pad_from_left
-      pad_from_right
-      permute
-      rank_of_bit_set_at_index
-      read_bits_from_file
-      reset
-      reverse
-      runs
-      set_value
-      shift_left             (for non-circular left shift)
-      shift_right            (for non-circular right shift)
-      test_for_primality
-      unpermute
-      write_to_file
-      write_bits_to_fileobject

          ''',
      license='Python Software Foundation License',
      keywords='bit array, bit vector, bit string, logical operations on bit fields',
      platforms='All platforms',
      classifiers=['Topic :: Utilities', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.5'],
      packages=['BitVector']
)
