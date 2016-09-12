from __future__ import print_function
from redispartition import RedisCluster
from redispartition.decorators import pipeiflist
import itertools


class Rhd(RedisCluster):

    def __init(self, connections):
        super().__init__(connections)

    def _index_to_mask_index(self, k):
        if not "mask" in k:
            if isinstance(k, list):
                return ["".join([str(i), "_mask"]) for i in k]
            else:
                return "".join([str(k), "_mask"])
        else:
            return k

    @pipeiflist
    def setbit(self, k, i, bit, with_mask=True, conn=None):
        if with_mask:
            self.setbit_mask(k, i, 1)
        return conn.setbit(k, i, bit)

    def set_mask(self, k, _bytes):
        k = self._index_to_mask_index(k)
        self.set(k, _bytes)

    def setbit_mask(self, k, i, bit):
        k = self._index_to_mask_index(k)
        self.setbit(k, i, bit, with_mask=False)

    def get_mask(self, k):
        k = self._index_to_mask_index(k)
        return self.get(k)

    def getbit_mask(self, k, i):
        k = self._index_to_mask_index(k)
        return self.getbit(k, i)

    def masked_xor(self, k1, k2):
        xorkey = "".join(["xor", k1, k2])
        self.bitop("XOR", xorkey, k1, k2)
        mask1 = self._index_to_mask_index(k1)
        mask2 = self._index_to_mask_index(k2)
        xorandkey = "".join(["andxor", mask1, mask2])
        self.bitop("AND", xorandkey, xorkey, mask1, mask2)
        return xorandkey

    def hamming_dist(self, k1, k2):
        masked_xor_key = self.masked_xor(k1, k2)
        hdist = self.bitcount(masked_xor_key)
        return hdist

    def distance_matrix(self, *args):
        matrix = [[0 for _ in range(len(args))] for _ in range(len(args))]
        for i, j in itertools.combinations([x for x in range(len(args))], 2):
            dist = self.hamming_dist(args[i], args[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
        return matrix
