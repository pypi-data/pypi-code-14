"""

AltimPy
=======

Purpose 
-------

Tools for manipulating and processing high-resolution along-track altimetric data

List of available functions
---------------------------
acknowledgments Return the information necessary to aknowledge the use of this software
atrous1d        One-dimensional wavelet transform using the a trous algorithm
deriv           Compute the derivative using centered differences with 9p stencil length
distrack        Compute the distance along satellite track
filter1d        Filter one-dimensional data
lanczos         Compute the lanczos filter
noise_model     Return the standrad deviation of noise using SWH as input
range_comp      Reduce resolution using range compression
velocity        Compute the geostrophic velocity after denoising altimetric data
wvdenoise       Denoise altimetric measurements using wavelets

History
-------
November 2016, J. Isern-Fontanet, Initial version

Authors
-------
J. Isern-Fontanet, e-mail: jisern@icm.csic.es
Barcelona Expert Centre in Remote Sensing (CSIC, UPC), Barcelona
Institut de Ciencies del Mar (CSIC), Barcelona

"""

####################################################################################################
# Imports

import numpy as np
import scipy.optimize as opt

####################################################################################################
# General information

__ModuleVersion__ = '0.1'

# Physical constants

Omega = 7.272205216e-5        # [1/s] Earh angular velocity
EarthRadius = 6371000.0       # [m] Earth radius
g = 9.8                       # [m/s^2] Gravity

# Mathematical constants

rtod = 180. / np.pi           # Radiants to degrees
dtor = np.pi / 180.           # Degrees to radiants


####################################################################################################

def acknowledgments():
    msg = \
        ("\n"
         "If you use this software please cite the following article:\n"
         "\n"
         "    J. Isern-Fontanet, R. Escola, C. Martin-Puig and M. Roca (2017). Extraction of high-\n"
         "    resolution geostrophic velocities from along-track altimetric measurements.\n"
         "    Submitted to Rem. Sens. Env.\n")

    return(msg)


####################################################################################################

def atrous1d(signal, wavelet='B3-Splines'):
    """
    W = atrous1d(S)
    
    Purpose: 
        Perform the one-dimensional wavelet transform using the a trous algorithm as described in 
        Starck & Murtagh (2012). Handbook of Astronomical Data Analysis. Springer-Verlag, 303pp.
    
    Input:
        A NumPy array of N points (S)
    Output: 
        A NumPy array with J+1 rows and N columns (W). The filtered signal at scale J is stored at W[0,:], 
        while the wavelet coefficients at scales j = 1,...,J are stored at W[0,:],...,W[J,:], where J 
        is the maximum scale computed.
    """

    # Choose the wavelet.

    if wavelet == 'B3-Splines':
        wfilter = np.array([1, 4, 6, 4, 1]) / 16.
        index = np.array([-2, -1, 0, 1, 2])
    else:
        wfilter = np.array([1, 4, 6, 4, 1]) / 16.
        index = np.array([-2, -1, 0, 1, 2])

    # Initialize

    N = len(signal)
    Nscale = np.int(np.floor(np.log(N) / np.log(2))) - 2

    W = np.zeros((Nscale + 1, N))
    C = np.zeros((Nscale + 1, N))
    C[0, :] = signal

    # Loop on scales

    for j in np.arange(Nscale):
        # Build the filter for this scale

        IndexStep = index * 2 ** j
        IndexStep = IndexStep - np.min(IndexStep)

        FilterStep = np.zeros(np.max(IndexStep) + 1)
        FilterStep[IndexStep] = wfilter

        # Convolve. Points beyond boundaries are assumed to be zero.

        C[j + 1, :] = np.convolve(C[j, :], FilterStep, mode='same')

        # Compute the Wavelet coefficients at sclae j+1

        W[j + 1, :] = C[j, :] - C[j + 1, :]

    # Returning

    W[0, :] = C[-1, :]

    return(W)


####################################################################################################

def deriv(d, f):
    f4fwd = np.roll(f, -4)
    f3fwd = np.roll(f, -3)
    f2fwd = np.roll(f, -2)
    f1fwd = np.roll(f, -1)
    f4bwd = np.roll(f, +4)
    f3bwd = np.roll(f, +3)
    f2bwd = np.roll(f, +2)
    f1bwd = np.roll(f, +1)

    # Compute the derivatives using all stencil lengths

    df1pfwd = (f1fwd - f) / d
    df1pbwd = (f - f1bwd) / d
    df3p = (f1fwd - f1bwd) / (2 * d)
    df5p = (-f2fwd + 8 * f1fwd - 8 * f1bwd + f2bwd) / (12 * d)
    df7p = (f3fwd - 9 * f2fwd + 45 * f1fwd - 45 * f1bwd + 9 * f2bwd - f3bwd) / (60 * d)
    df9p = (-3 * f4fwd + 32 * f3fwd - 168 * f2fwd + 672 * f1fwd -
            672 * f1bwd + 168 * f2bwd - 32 * f3bwd + 3 * f4bwd) / (840 * d)

    # Fill boundary values

    df = df9p
    df[3] = df7p[3]
    df[-4] = df7p[-4]
    df[2] = df5p[2]
    df[-3] = df5p[-3]
    df[1] = df3p[1]
    df[-2] = df3p[-2]
    df[0] = df1pfwd[0]
    df[-1] = df1pbwd[-1]

    return(df)

####################################################################################################

def distrack(lat, lon):
    """
    d = distrack(lon,lat)
    
    Purpose:
        Compute the distance between points along the major circle conecting them
    
    Input:
        NumPy arrays with longitude (lon) and latitude (lat)
    
    Output:
        NumPy array with the distance in m between points along the major circle conecting them
    """

    dlat = (lat - np.roll(lat, +1)) * dtor
    dlon = (lon - np.roll(lon, +1)) * dtor

    d = EarthRadius * np.arccos(np.cos(dlon) * np.cos(dlat))
    d[0] = 0

    return(d)


####################################################################################################

def filter1d(signal, sampling, Lmin=0, Lmax=0):
    """
    Filter using a Lancvzos filter
    """
    si = np.concatenate((signal, signal[::-1]))
    N = len(si)

    # Fourier transform

    k = 2 * np.pi * np.arange(N // 2 + 1) / N / sampling
    kn = np.max(k)
    fs = np.fft.rfft(si)

    # Apply the filter

    if Lmin > 0:
        kmax = 2 * np.pi / Lmin
        low_pass = lanczos(k, kmax, kn)
    else:
        low_pass = np.ones(len(k))

    if Lmax > 0:
        kmin = 2 * np.pi / Lmax
        high_pass = (1 - lanczos(k, kmin, kn))
    else:
        high_pass = np.ones(len(k))

    fs = fs * high_pass * low_pass

    # Inverse transform

    N = N//2
    so = np.fft.irfft(fs)
    so = so[0:N]

    return(so)

####################################################################################################

def lanczos(k, kc, kn):
    """
    Lanczos filter
    """
    M = 300
    fcl = kc / kn
    for j in np.arange(M)+1:
        fcl = fcl + 2 * kc / kn * (np.sin(np.pi * j / M) / (np.pi * j / M)) * \
              (np.sin(np.pi * j * kc / kn) / (np.pi * j * kc / kn)) * \
              np.cos(np.pi * j * k / kn)

    return(fcl)

####################################################################################################

def noise_model(swh, profile):
    # Select the profile name

    if profile == 'CS2-20Hz ':
        prfnum = 1
    elif profile == 'J1-1Hz':
        prfnum = 2
    elif profile == 'J2-1Hz':
        prfnum = 2
    else:
        prfnum = 1

    # Compute the standard deviation of noise

    if prfnum == 1:
        a = 0.0526846
        b = -0.00390969
        c = 0.00233301
        d = -0.000169097
        e = 3.38643e-06
        noise = a + b * swh + c * swh ** 2 + d * swh ** 3 + e * swh ** 4  # [m]
    elif prfnum == 2:
        a = 0.0153602
        b = -0.000465942
        c = 0.00124970
        d = -0.000129152
        e = 3.59554e-06
        noise = a + b * swh + c * swh ** 2 + d * swh ** 3 + e * swh ** 4  # [m]
    else:
        noise = np.zeros(len(swh))

    return(noise)


####################################################################################################

def range_comp(hin, Nb, xin, mask=[False]):
    """
    res = range_comp(Hin, Nb, Xin)
    
    Purpose:
        Reduce the resolution of measurements sampled at regular intervals through binning the data 
        and using robust fiting

    Input:
        NumPy one-dimensional array with the data
    """

    Nin = len(xin)

    # Build a mask if it has not been provided

    if not mask[0]:
        msk = np.ones(Nin, dtype=bool)
    elif len(mask) < Nin:
        msk = np.ones(Nin, dtype=bool)
        msk[0:len(mask)] = mask
    elif len(mask) > Nin:
        msk = mask[0:Nin]
    else:
        msk = mask

    # Determine the limits of bins

    bwd = np.int(np.floor(Nb / 2.))
    fwd = np.int(np.ceil(Nb / 2.))

    i = np.arange(bwd, Nin - fwd, Nb, dtype=np.int)
    imin = i - bwd
    imax = i + fwd

    Nout = np.int(np.floor(Nin / Nb))

    # Loop on bins

    func = lambda a, xx, yy: a[0] + a[1] * xx - yy  # Define the function that provides the residuals

    slope = np.zeros(Nout)
    intercept = np.zeros(Nout)
    xc = np.zeros(Nout)
    hc = np.zeros(Nout)
    mc = np.zeros(Nout, dtype=bool)

    for j in np.arange(Nout):

        x = xin[imin[j]:imax[j]]
        y = hin[imin[j]:imax[j]]
        m = msk[imin[j]:imax[j]]
        xc[j] = xin[i[j]]

        N = np.sum(m)

        if N > 5:
            mc[j] = True

            # Robust fitting

            a = np.ones(2)
            res = opt.least_squares(func, a, args=(x[m], y[m]), loss='soft_l1', f_scale=0.01)

            # Estimate the SLA at the desired point

            intercept[j] = res.x[0]
            slope[j] = res.x[1]
            hc[j] = xc[j] * slope[j] + intercept[j]

    # Return

    return(hc, xc, (imin, imax, slope, intercept))

####################################################################################################

def velocity(ssh_, lat_, lon_, swh_, rossby=0, profile='j2-1Hz'):
    # Prepare the data

    N = len(ssh_)
    ssh = ssh_.copy()
    lat = lat_.copy()
    lon = lon_.copy()

    # Compute distances, assumes no gaps and constant sampling

    dx = np.mean(np.abs(distrack(lat, lon)))

    # Build SWH and smooth them

    if type(swh_) is np.ndarray:
        if len(swh_) < N:
            swh = np.zeros(N) + swh_[0]
        else:
            swh = swh_[0:N]
            swh = filter1d(swh, dx, Lmin=100e3)
    else:
        swh = np.zeros(N) + swh_

    # Reverse the profile, if necessary

    if lat[0] > lat[-1]:
        reverse = True
        ssh = ssh[::-1]
        swh = swh[::-1]
    else:
        reverse = False

    # Get noise standard deviation

    noise = noise_model(swh, profile)

    # Denoise

    sshh = wvdenoise(ssh, noise, thresholding='hard', k=3)
    sshs = wvdenoise(ssh, noise, thresholding='soft', k=3)

    # Correct the energy level of soft thresholding

    sshs = sshs * np.mean(sshh * sshs) / np.mean(sshs ** 2)

    # Low-pass filtering removing scales below the Rossby radius

    sshf = filter1d(sshs, dx, Lmin=rossby)

    # Compute velocities

    lat0 = np.mean(lat)
    f0 = 2 * Omega * np.sin(lat0 * dtor)
    vg = - deriv(dx, sshf) * g / f0

    #  Return

    if reverse:
        sshf = sshf[::-1]
        vg = vg[::-1]


    return(sshf, vg)


####################################################################################################

def wvdenoise(signal, noise, wavelet='B3-Splines', k=3, thresholding='hard'):
    """
    res = wvdenoise(signal, noise, WaveletName='B3-Splines', k=3, thresholding='hard'):
    
    Purpose:
        Remove noise from a data time series
        

    Input:
        NumPy one-dimensional array with the data
    """

    # Choose the wavelet.

    if wavelet == 'B3-Splines':
        sigmae = np.array(
                  [0.723625518248,  0.285511349331,  0.177761698711,
                   0.121908619832,  0.0858608370413, 0.0606387633654,
                   0.0428876700367, 0.0302561895430, 0.0214925354358,
                   0.0151090102106, 0.0105969740186, 0.00739901691508,
                   0.00516253257288, 0.00346755834812, 0.00249045645907])
    else:
        sigmae = np.zeros(15)

    # Wavelet decomposition, first row corresponds to the low-pass filtered signal

    w = atrous1d(signal, wavelet=wavelet)
    Nlev, Np = w.shape

    # Threshold value at each level

    sigmae = np.roll(sigmae[0:Nlev], +1)
    sigmae[0] = 0
    sigma, sigmae = np.meshgrid(noise, sigmae)
    Th = sigma * sigmae
    Th[1:, :] = k * Th[1:, :]

    # Thresholding

    M = np.ones(w.shape)
    M[np.abs(w) < Th] = 0

    # Reconstruct

    if thresholding == 'hard':
        recs = np.sum(M * w, axis=0)
    elif thresholding == 'soft':
        recs = np.sum(np.sign(w) * (np.abs(w) - Th) * M, axis=0)
    else:
        recs = np.sum(w, axis=0)

    return(recs)


####################################################################################################

print("Module ", __name__, " (version " + __ModuleVersion__ + ")")
print((len(__name__) + 8) * "-")
print('Barcelona Expert Centre in Remote Sensing')
print('Institut de Ciencies del Mar (CSIC)')
print(acknowledgments())
