
import numpy as np
import matplotlib.cm as cm


class RandomColor(object):

    @classmethod
    def _hex(Cls, num, length=4):
        hexx = hex(num)
        hexx += '0' * (length - len(hexx))
        assert len(hexx) == length
        return hexx.upper()[2:]

    @classmethod
    def _str_format(Cls, r, g, b):
        return "#{}{}{}".format(Cls._hex(r), Cls._hex(g), Cls._hex(b))

    @staticmethod
    def sample_rgb():
        return RandomColor._str_format(np.random.randint(17, 256),
                                       np.random.randint(17, 256),
                                       np.random.randint(17, 256))

    @staticmethod
    def sample_map(cmap=None):
        if cmap is None:
            cmap = cm.jet
        r, g, b, _ =  cmap(np.random.rand())
        return RandomColor._str_format(int(255*r), int(255*g), int(255*b))


