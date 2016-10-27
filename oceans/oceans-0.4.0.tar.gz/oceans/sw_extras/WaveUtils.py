"""

The Waves.py module contains an assortment of tools for working with
linear wave theory calculations.

"""

import numpy as np

twopi = 2*np.pi


def WaveNumber(g, omega, h):
    p = omega**2 * h / g
    q = Dispersion(p)
    k = q * omega**2 / g
    return k


def Frequency(g, k, h):
    omega = np.sqrt(g*k*np.tanh(k*h))
    return omega


def Dispersion(p, Tol=1e-14, MaxIter=100):
    """

    finds q, given p

    q = gk/omega^2     non-d wave number
    p = omega^2 h / g   non-d water depth

    """
    # First guess (from Fenton and McKee):
    q = np.tanh(p**0.75)**(-2.0/3.0)

    iter = 0
    f = q * np.tanh(q*p) - 1
    while abs(f) > Tol:
        qp = q*p
        fp = qp / (np.cosh(qp)**2) + np.tanh(qp)
        q = q - f/fp
        f = q * np.tanh(q*p) - 1
        iter += 1
        if iter > MaxIter:
            raise Exception("Maximum number of iterations reached.")
    return q


def Max_u(a, omega, g, h, z):
    k = WaveNumber(g, omega, h)
    u = a * omega * (np.cosh(k*(h+z)) / np.sinh(k*h))
    return u


def AmpScaleAtDepth(g, omega, h, z):
    k = WaveNumber(g, omega, h)
    return np.cosh(k*(h+z)) / np.cosh(k*(h))


def Celerity(omega, k, h, g):
    C = np.sqrt(g/k * np.tanh(k*h))
    return C


def GroupSpeed(omega, k, h, g):
    n = 1.0/2 * (1 + (2*k*h / np.sinh(2*k*h)))
    Cg = n * Celerity(omega, k, h, g)
    return Cg


def ShoalingCoeff(omega, g, h0, h2):
    """
    Compute the shoaling coeff for two depths: ho and h1.
    Pass in h0 = None for deep water

    """
    k2 = WaveNumber(g, omega, h2)
    Cg2 = GroupSpeed(omega, k2, h2, g)
    if h0 is not None:
        k0 = WaveNumber(g, omega, h0)
        Cg0 = GroupSpeed(omega, k0, h0, g)
        Ks = np.sqrt(Cg0/Cg2)
        return Ks
    else:  # Deep water.
        return np.sqrt((g / (2*omega)) / Cg2)


def ReadNDBCSpectrum(filename):
    """
    Note: this ignores gaps in the data

    """

    with open(filename, 'r') as infile:
        header = infile.readline()
        bins = np.array([float(x) for x in header.split()[4:]])
        # print("bins: {}".format(bins))
        Dates = []
        Data = []
        for line in infile:
            Data.append([float(x) for x in line.split()[4:]])
            Dates.append(line.split()[:4])
    Data = np.array(Data, np.Float)
    return (bins, Data, Dates)


def ReadNDBCSpectrumRealTime(filename, verbose=False):
    """
    This reads the "real time" NDBC data, which is a different format than
    the archive data.

    Note: this ignores gaps in the data

    """

    with open(filename, 'r') as infile:
        header = infile.readline()
        if verbose:
            print(header)
        # bins = np.array([float(x) for x in header.split()[4:]])
        # print("bins: {}".format(bins))

        Dates = []
        Data = []
        Bins = []
        for line in infile:
            Dates.append(line.split()[:4])
            data = line.split()[6:]
            Data.append([float(data[i]) for i in range(0, len(data), 2)])
            if not Bins:
                Bins = ([float(data[i][1:-1]) for i in range(1, len(data), 2)])

    Data = np.array(Data, float)
    Bins = np.array(Bins, float)
    return (Bins, Data, Dates)


if __name__ == "__main__":
    import pylab

    # print("Computing velocity at the bottom")
    # print("Please use all SI units")

    # g = 9.806

    # H = input("Wave height? =>")
    # h = input("Depth ? =>")
    # T = input("Period? =>")

    # a = H/2
    # omega = twopi/T
    # z = -h

    # k = WaveNumber(g, omega, h)
    # MaxU = Max_u(a, omega, g, k, h, z)

    # print("the maximum velocity at the bottom is: {:%f} m/s".format(MaxU))
    # print("Computing velocity at the bottom")
    # print("Please use all SI units")

    g = 9.806
    h = 55

    print("In a water depth of 55m (180ft): ")

    k = twopi / (2 * h)

    omega = Frequency(g, k, h)

    T = twopi / omega

    print("The minimum period of waves affecting the "
          "bottom is {:%f} seconds".format(T))

    print("the shoaling coeff is:")
    print(ShoalingCoeff(omega, g, None, h))
    print("Which is negligible")

    # bins, Es = ReadNDBCSpectrum("46042w2004.txt")
    bins, Es, dates = ReadNDBCSpectrum("Winter2004.txt")

    print("Periods: {}".format(1 / bins))
    # Convert bins (Hz) to k:
    omega = twopi * bins
    k = WaveNumber(g, omega, h)

    print("Wave Numbers: {}".format(k))

    # Convert to energy at the bottom:
    Eb = Es / (np.sinh(k*h)**2)

    print("Energy at Top:")
    print(Es[0:1])
    print("Energy at Bottom:")
    print(Eb[0:1])
    # print("Ratio:")
    # print(Eb[0:1] / Es[0:1])

    # Total energy.
    Etotal = np.sum(Eb, 1)  # Sum across rows,

    # Plot energy:
    # pylab.contour(1/bins, np.arange(len(Eb)), Eb)
    # pylab.xlabel("Period")
    # pylab.show()

    pylab.figure(2)
    pylab.contour(1/bins, np.arange(50), Eb[1330:1380, :])
    pylab.xlabel("Period")
    pylab.show()

    # Find the Maximum.
    MaxTime = np.argmax(Etotal)
    print("time of max Energy")
    print(dates[MaxTime])
    MaxDay_s = Es[MaxTime]
    MaxDay_b = Eb[MaxTime]

    # Equivalent wave height.
    # This assumes the bins are all the same size!
    domega = omega[1] - omega[0]
    dHz = bins[1] - bins[0]
    # print("domega: {}".format(domega))

    Hmax_s = np.sqrt(8 * MaxDay_s * domega)
    Hmax_b = np.sqrt(8 * MaxDay_b * domega)
    # Hmax_s = np.sqrt(8 * MaxDay_s * dHz)
    # Hmax_b = np.sqrt(8 * MaxDay_b * dHz)
    print("Hmax_s: {}".format(Hmax_s))
    print("Hmax_b: {}".format(Hmax_b))

    Umax_s = Hmax_s / 2*omega
    Umax_b = Hmax_b / 2*omega

    Umax_s2 = Max_u(Hmax_s/2, omega, g, k, h, z=0)
    Umax_b2 = Max_u(Hmax_s/2, omega, g, k, h, z=-h)

    print("Umax_b: {}".format(Umax_b))

    MaxU_i = np.argmax(Umax_b)

    print("During a storm on {}".format(dates[MaxTime]))
    print("Maximum Wave height is: {:.2f}".format(Hmax_s[MaxU_i]))

    print("Maximum velocity at the surface is {:.2f}"
          "m/s:".format(Umax_s[MaxU_i]))
    print("Maximum velocity at bottom is {:.2f} m/s:".format(Umax_b[MaxU_i]))

    print("Maximum velocity at the surface is {:.2f}"
          "m/s:".format(Umax_s2[MaxU_i]))
    print("Maximum velocity at bottom is {:.2f} m/s:".format(Umax_b2[MaxU_i]))

    print("At a period of {:.1f} seconds".format((twopi/omega[MaxU_i])))
    print("The Wavelength at that period is {:.1f}"
          "meters".format((twopi/k[MaxU_i])))
