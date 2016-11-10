import numpy as np
import matplotlib.pyplot as plt

from mimircache import pardaProfiler
from mimircache.cacheReader.plainReader import plainReader
from mimircache.cacheReader.vscsiReader import vscsiReader


def FFT(dat):
    rd = np.array(dat)
    print(rd)
    sp = np.fft.fft(rd)
    print(sp)

    n = len(sp)  # length of the signal
    # k = np.arange(n)
    # T = n / Fs
    # frq = k / T  # two sides frequency range
    # frq = frq[range(n / 2)]  # one side frequency range

    freq = np.fft.fftfreq(n)

    # plt.plot(freq, sp.real, freq, sp.imag)
    # plt.plot(freq[1:len(freq)/2-1], np.abs(sp)[1:len(freq)/2-1])
    plt.semilogy(freq[1:len(freq) / 2 - 1], np.abs(sp)[1:len(freq) / 2 - 1])

    plt.savefig('test.png')
    # for i in rd:
    #     print(i)


def FFT_cache():
    # p = pardaProfiler(30000, plainCacheReader("../data/parda.trace"))
    p = pardaProfiler(30000, vscsiReader("../data/trace_CloudPhysics_bin"))

    # p = pardaProfiler(30000, vscsiCacheReader("../data/cloudphysics/w64_vscsi2.vscsitrace"))
    rd_c = p.get_reuse_distance()
    rd = []
    m = np.mean(rd_c)
    print(m)
    # for i in rd_c:
    #     print(i)
    for i in rd_c:
        if i != -10:
            rd.append(i)

    FFT(rd)


def FFT_test():
    import random
    l = []
    for i in range(1000000):
        l.append(random.randint(1, 1000))
    FFT(l)


def test1():
    p = pardaProfiler(30000, vscsiReader("../data/trace_CloudPhysics_bin"))
    rd_c = p.get_reuse_distance()
    plt.plot(rd_c)
    plt.savefig('rd.png')


def test2():
    t = np.arange(256)
    sp = np.fft.fft(np.sin(t))
    freq = np.fft.fftfreq(t.shape[-1])
    # plt.plot(freq, sp.real, freq, sp.imag)
    plt.plot(sp.real, sp.imag)
    # plt.show()
    plt.savefig('test2.png')


# FFT_test()
# FFT_cache()
# test2()
test1()
