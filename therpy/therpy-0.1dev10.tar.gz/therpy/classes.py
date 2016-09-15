# Define classes

# Imports
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as spintp

# Importing from therpy is its main else using .
if __name__ == '__main__':
    import os.path
    import sys

    path2therpy = os.path.join(os.path.expanduser('~'), 'Documents', 'My Programs', 'Python Library')
    sys.path.append(path2therpy)
    from therpy import smooth
    from therpy import calculus
    from therpy import imageio
    from therpy import imagedata
    from therpy import constants
    from therpy import functions
else:
    from . import smooth
    from . import calculus
    from . import imageio
    from . import imagedata
    from . import constants
    from . import functions


# import smooth
# import calculus

# Curve class for 1D functions
class Curve:
    """
    class for generic function f(xi) = yi

    Properties:
        x, y, data, dx, sorti

    Methods:
        __call__
        inverse (in progress)
        loc (in progress)
        sortbyx : returns sorted (x,y)
        binbyx : returns binned (x,y)
        subsample : returns sub sampled (x,y)
        diff (in progress)
        int (in progress)
    """

    def __init__(self, x=None, y=np.array([]), **kwargs):
        if x is None: x = np.arange(y.size)
        self.var = kwargs
        self.var['x'] = x.copy()
        self.var['y'] = y.copy()

    ### Properties ###

    @property
    def x(self):
        return self.var.get('x', np.array([]))

    @property
    def y(self):
        return self.var.get('y', np.array([]))

    @property
    def yfit(self):
        return self.var.get('yfit', None)

    @property
    def fitusing(self):
        return self.var.get('fitusing', None)

    @property
    def xyfitplot(self):
        return self.var.get('xyfitplot', None)

    @property
    def sorti(self):
        sorti = self.var.get('sorti', None)
        if sorti is None:
            sorti = np.argsort(self.x)
            self.var['sorti'] = sorti
        return sorti

    @property
    def dx(self):
        return (self.x[1] - self.x[0])

    @property
    def data(self):
        return (self.x, self.y)

    @property
    def plotdata(self):
        return (self.x / self.xscale, self.y / self.yscale)

    @property
    def xscale(self):
        return self.var.get('xscale',1)

    @property
    def yscale(self):
        return self.var.get('yscale', 1)

    @property
    def miny(self): return np.min(self.y)

    @property
    def maxy(self): return np.max(self.y)

    @property
    def minx(self): return np.min(self.x)

    @property
    def maxx(self): return np.max(self.x)

    ### High level methods ###
    def __call__(self, xi):
        return np.interp(xi, self.x[self.sorti], self.y[self.sorti])

    def __str__(self):
        des = 'A curve with ' + str(self.x.size) + ' data points.'
        return des

    def inverse(self, yi):
        pass

    def loc(self, x=None, y=None):
        if x != None:
            return self.locx(x)
        elif y != None:
            return self.locy(y)
        else:
            print('ERROR: Please provide x or y')
        return 0

    def chop(self,xlim=None,ylim=None):
        return self.trim(xlim, ylim)

    def subset(self, xlim=None, ylim=None):
        return self.trim(xlim, ylim)

    def trim(self,xlim=None,ylim=None):
        # Prepare using
        using = np.array(np.ones_like(self.x), np.bool)
        if xlim is not None:
            using[self.x < xlim[0]] = False
            using[self.x > xlim[1]] = False
        if ylim is not None:
            using[self.y < ylim[0]] = False
            using[self.y > ylim[1]] = False
        if np.sum(using) <= 2:
            using = np.array(np.ones_like(self.x), np.bool)
            print("X and Y limits given leads to too little points. All are being used")
        return self.copy(self.x[using], self.y[using])

    def sortbyx(self):
        return self.copy(self.x[self.sorti], self.y[self.sorti])

    def binbyx(self, **kwargs):
        return self.copy(*smooth.binbyx(self.x, self.y, **kwargs))

    def subsample(self, bins=2):
        return self.copy(*smooth.subsampleavg(self.x, self.y, bins=bins))

    def diff(self, **kwargs):
        method = kwargs.get('method', 'poly')
        if method == 'poly':
            dydx = calculus.numder_poly(self.x, self.y, order=kwargs.get('order', 1), points=kwargs.get('points', 1))
        elif method == 'central2':
            dydx = np.gradient(self.y, self.dx, edge_order=2)
        return self.copy(self.x, dydx)

    def removenan(self):
        self.var['x'] = self.x[np.isfinite(self.y)]
        self.var['y'] = self.y[np.isfinite(self.y)]

    def copy(self, x=None, y=None):
        if x is None: x = self.x
        if y is None: y = self.y
        return Curve(x=x, y=y, xscale=self.xscale, yscale=self.yscale)

    def fit(self, fitfun, guess, plot=False, pts=1000, noise=None, loss='cauchy', bounds=(-np.inf, np.inf), xlim=None, ylim=None):
        # Prepare using
        using = np.array(np.ones_like(self.x), np.bool)
        if xlim is not None:
            using[self.x<xlim[0]] = False
            using[self.x>xlim[1]] = False
        if ylim is not None:
            using[self.y<ylim[0]] = False
            using[self.y>ylim[1]] = False
        if np.sum(using) <= len(guess):
            using = np.array(np.ones_like(self.x), np.bool)
            print("X and Y limits given leads to too little points. All are being used")

        # Fit
        if noise is None:
            from scipy.optimize import curve_fit
            try:
                fitres, fiterr = curve_fit(fitfun, self.x[using], self.y[using], p0=guess, bounds=bounds)
                fiterr = np.sqrt(np.diag(fiterr))
            except RuntimeError as err:
                fitres = guess
                fiterr = guess
                print("CAN'T FIT, Returning Original Guess: Details of Error {}".format(err))
        else:
            from scipy.optimize import least_squares
            try:
                fitfun_ = lambda p: fitfun(self.x[using], *p) - self.y[using]
                fitres_ = least_squares(fun=fitfun_, x0=guess, loss=loss, f_scale=noise, bounds=bounds)
                fitres = fitres_.x
                fiterr = np.zeros_like(guess) * np.nan
            except RuntimeError as err:
                fitres = guess
                fiterr = np.zeros_like(guess) * np.nan
                print("CAN'T FIT, Returning Original Guess: Details of Error {}".format(err))

        yfit = fitfun(self.x, *fitres)
        xfitplot = np.linspace(np.min(self.x), np.max(self.x), pts)
        yfitplot = fitfun(xfitplot, *fitres)
        # Save results in var
        self.var['fitusing'] = using
        self.var['yfit'] = yfit
        self.var['xyfitplot'] = (xfitplot, yfitplot)
        self.var['fitres'] = fitres
        self.var['fiterr'] = fiterr
        # Plot and display
        if plot:
            # Plot
            plt.figure(figsize=(5, 5))
            ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
            ax2 = plt.subplot2grid((3, 1), (2, 0))
            ax1.plot(*self.xyfitplot,'k-')
            ax1.plot(self.x, self.y, 'g.')
            ax1.plot(self.x[using], self.y[using],'r.')
            ax2.plot(self.x, self.y-self.yfit,'g.')
            ax2.plot(self.x[using], self.y[using] - self.yfit[using], 'r.')
            ax2.vlines(self.x, self.x*0, self.y-self.yfit)
            plt.xlabel('x')
            plt.ylabel('Difference')
            # Print
            print("##______Fit Value______Error______")
            for i,val in enumerate(fitres):
                print("{:2d} ==> {:9.4} (+-) {:9.4}".format(i, fitres[i], fiterr[i]))
        # return fitresults
        return (fitres, fiterr)

    ### Low level methods ###
    def locx(self, xi):
        x = self.x[self.sorti]
        iloc = np.argwhere(x <= xi)
        if len(iloc) == 0:
            return 0
        elif len(iloc) == x.size:
            return x.size - 1
        else:
            iloc = iloc[-1, 0]
        if (xi - x[iloc]) >= (x[iloc + 1] - xi): iloc += 1
        return iloc

    def locy(self, yi):
        pass

    def int(self, **kwargs):
        method = kwargs.get('method', 'sum')
        self.xInt = self.xLatest
        self.yInt = self.yLatest
        if method == 'sum':
            self.Int = np.sum(self.y) * self.dx
        return self.Int


# Absorption Image Class
class AbsImage():
    '''
    Absorption Image Class

    Inputs:
        one of the three ways to define an image
        constants object (default is Li 6 Top Imaging)


    Inputs (Three ways to define an image):
        1) name (image filename with date prefix)
        2) wa and woa (numpy arrays)
        3) od (numpy array)
    cst object
    '''

    def __init__(self, *args, **kwargs):
        # Create a dict var to store all information
        self.var = kwargs
        self.cst = kwargs.get('cst', constants.cst())
        # Check the args
        if len(args) > 0 and type(args[0]) is str: self.var['name'] = args[0]

    # Universal Properties
    @property
    def wa(self):
        if 'wa' not in self.var.keys():
            alldata = self.alldata
            self.var['wa'] = alldata[0]
            self.var['woa'] = alldata[1]
        return self.var.get('wa')

    @property
    def woa(self):
        if 'woa' not in self.var.keys():
            alldata = self.alldata
            self.var['wa'] = alldata[0]
            self.var['woa'] = alldata[1]
        return self.var.get('woa')

    @property
    def od(self):
        if 'od' not in self.var.keys():
            self.var['od'] = (self.rawod * self.cst.ODf) + ((self.woa - self.wa) / self.cst.Nsat)
        return self.var['od']

    @property
    def rawod(self):
        if 'rawod' not in self.var.keys():
            self.var['rawod'] = imagedata.get_od(self.wa, self.woa, rawod=True)
        return self.var['rawod']

    @property
    def fixod(self):
        if 'fixod' not in self.var.keys():
            rawod = imagedata.get_od(self.wa, self.woa, width=self.var.get('trouble_pts_width', 5), rawod=False)
            self.var['fixod'] = (rawod * self.cst.ODf) + ((self.woa - self.wa) / self.cst.Nsat)
        return self.var['fixod']

    @property
    def ncol(self):
        return self.od / self.cst.sigma

    @property
    def atoms(self):
        return self.ncol * self.cst.pixel ** 2

    @property
    def total_atoms(self):
        return np.sum(self.atoms)

    @property
    def xy(self):
        x = np.arange(self.wa.shape[1])
        y = np.arange(self.wa.shape[0])
        return np.meshgrid(x, y)

    # Properties special for fits images
    @property
    def name(self):
        return self.var.get('name', 'NotGiven')

    @property
    def path(self):
        return imageio.imagename2imagepath(self.name)

    @property
    def rawdata(self):
        return imageio.imagepath2imagedataraw(self.path)

    @property
    def alldata(self):
        return imageio.imagedataraw2imagedataall(self.rawdata)

    # Crop index function
    def cropi(self, **kwargs):
        cropi = imagedata.get_cropi(self.od, **kwargs)
        if kwargs.get('plot',False):
            x = [cropi[1].start,cropi[1].start,cropi[1].stop,cropi[1].stop,cropi[1].start]
            y = [cropi[0].start,cropi[0].stop,cropi[0].stop,cropi[0].start,cropi[0].start]
            fig, ax = plt.subplots(figsize=(7,3),ncols=2)
            ax[0].imshow(self.od, cmap='viridis', clim=kwargs.get('odlim',(0,2)), origin='lower')
            ax[0].plot(x, y,'w-')
            ax[0].set(xlim=[0,self.od.shape[1]], ylim=[0,self.od.shape[0]])
            ax[1].imshow(self.od[cropi], cmap='viridis', clim=kwargs.get('odlim',(0,2)), origin='lower')
            ax[1].set(xlim=[0, self.od[cropi].shape[1]], ylim=[0, self.od[cropi].shape[0]])
        return cropi

    # fix intensities
    def fixVaryingIntensities_AllOutside(self, xmin, xmax, ymin, ymax):
        # Define a crop region and find factor*woa
        (x,y) = self.xy
        cropi = np.logical_and.reduce((x>=xmin, x<=xmax, y>=ymin, y<=ymax))
        factor = np.sum(self.alldata[0][cropi==0]) / np.sum(self.alldata[1][cropi==0])
        self.var['factor_woa'] = factor
        # Recalculate wa, woa, od, fixod
        self.var['wa'] = self.alldata[0]
        self.var['woa'] = self.alldata[1] * self.var['factor_woa']
        if 'od' in self.var.keys(): del self.var['od']
        if 'fixod' in self.var.keys(): del self.var['fixod']
        if 'rawod' in self.var.keys(): del self.var['rawod']

    def fixVaryingIntensities_Box(self, cropi=None, **kwargs):
        # Define a crop region and find factor*woa
        (x,y) = self.xy
        if cropi is None: cropi = self.cropi(**kwargs)
        factor = np.sum(self.alldata[0][cropi]) / np.sum(self.alldata[1][cropi])
        self.var['factor_woa'] = factor
        # Recalculate wa, woa, od, fixod
        self.var['wa'] = self.alldata[0]
        self.var['woa'] = self.alldata[1] * self.var['factor_woa']
        if 'od' in self.var.keys(): del self.var['od']
        if 'fixod' in self.var.keys(): del self.var['fixod']
        if 'rawod' in self.var.keys(): del self.var['rawod']

    # Auto crop hybrid
    def autocrop_hybrid(self, plot=False, odlim=(0,2), border = 50):
        # along y
        c = Curve(y=np.nansum(self.od, axis=1))
        max_y = np.max(c.y[c.y.shape[0]//4:3*c.y.shape[0]//4])
        ind = np.argwhere(c.y == max_y)[0][0]
        guess = [c.x[ind], c.x.shape[0]/10, c.y[ind], c.y[ind]/10, c.y[ind]/100]
        fy = c.fit(functions.fitfun_TF_harmonic, guess, plot=False)[0]
        # along x
        c = Curve(y=np.nansum(self.od, axis=0))
        max_y = np.max(c.y[c.y.shape[0] // 4:3 * c.y.shape[0] // 4])
        ind = np.argwhere(c.y == max_y)[0][0]
        guess = [c.x[ind], c.x.shape[0] / 10, c.y[ind], c.y[ind] / 10, c.y[ind] / 100]
        fx = c.fit(functions.fitfun_TF_harmonic, guess, plot=False)[0]
        # Generate cropi
        center = (int(fx[0]),int(fy[0]))
        width = 2 * int(min(fx[1] * 2, center[0] - border, self.od.shape[1] - center[0] - border))
        height = 2 * int(min(fy[1] * 2, center[1] - border, self.od.shape[0] - center[1] - border))
        return self.cropi(center=center, width=width, height=height, plot=plot, odlim=odlim)

    # Averaging multiple images together
    def avgod(self, *args):
        avg = self.od
        for im in args: avg += im.od
        return avg / (1 + len(args))

    # pixels that are not usable are defined by:
    def usable(self, threshold=25):
        return imagedata.get_usable_pixels(self.wa, self.woa, threshold=threshold)

    # Fixing nan and inf
    # Example
    # indices = np.where(np.isnan(a)) #returns an array of rows and column indices
    # for row, col in zip(*indices):
    # a[row,col] = np.mean(a[~np.isnan(a[:,col]), col]) need to modify this

    # def interpolate_nans(X):
    # """Overwrite NaNs with column value interpolations."""
    # for j in range(X.shape[1]):
    # 	mask_j = np.isnan(X[:,j])
    # 	X[mask_j,j] = np.interp(np.flatnonzero(mask_j), np.flatnonzero(~mask_j), X[~mask_j,j])
    # return X


class XSectionTop:
    '''
    Compute Cross sectional area for a hybrid image using circular fits

    Inputs:
        od     --  cropped od image (od is recommanded because i know that amplitude is in range 0 to ~3)
        yuse   --  the range of y indices to use for fitting circles. Use np.arange(start, stop, step).
                   use None (or don't provide) to auto generate it
        method --  method for extending fitted radii: linead (default), poly4, spline
        plot   --  True or False, a sample plot with analysis, default False
        odlim  --  clim for imshow for the od, default (0,2)
        yset   --  settings for auto yuse: (y step, fraction of R_TF to use), default (10,0.75)
        guess  --  guess for circle fit: (x_center, radius, amplitude, m, b), default (xlen/2, xlen/5, max)

    Useful properties and calls:
        self(y_indices) returns area for provided y_indices. (must be within od size range)
        self.rad
        self.area
        self.yall
    '''
    def __init__(self, od, yuse = None, method='linear', plot=False, odlim=(0,2), yset = (10, 0.75), guess = None):
        self.prepare(od, yuse, odlim, yset, guess)
        self.fitall()
        if method == 'spline': self.extend_spline()
        elif method == 'poly4': self.extend_poly4()
        else: self.extend_linear()

        if plot: self.infoplot()

    def __call__(self, y):
        # Make it an integer
        y = np.int32(np.round(y))
        return self.area[y]

    def prepare(self, od, yuse, odlim, yset, guess):
        # General things
        self.yuse = yuse
        self.od = od
        self.odlim = odlim
        self.guess = guess
        self.yset_ = yset
        if yuse is None: yuse = self.get_yuse()
        self.dy = yuse[1] - yuse[0]
        # ycen_ vs. xc_, r_, xl_, xr_, c_
        self.ycen_ = yuse[0:-1] + self.dy / 2
        self.xc_, self.r_ = np.zeros_like(self.ycen_), np.zeros_like(self.ycen_)
        self.c_ = [None] * self.xc_.shape[0]
        self.fitres_ = [None] * self.xc_.shape[0]
        self.fiterr_ = [None] * self.xc_.shape[0]
        # yall vs rad, area
        self.yall = np.arange(od.shape[0])

    def fitall(self):
        if self.guess is None:
            c = Curve(y=np.nanmean(self.od[self.yuse[0]:self.yuse[0 + 1], :], axis=0))
            self.guess = [c.x.shape[0] / 2, c.x.shape[0] / 5, np.max(c.y), 0, 0]
        for i, yc in enumerate(self.ycen_):
            c = Curve(y=np.nanmean(self.od[self.yuse[i]:self.yuse[i + 1], :], axis=0))
            c.removenan()
            fitres, fiterr = c.fit(self.fitfun, self.guess, plot=False)
            self.xc_[i] = fitres[0]
            self.r_[i] = fitres[1]
            self.c_[i] = c
            self.fitres_[i] = fitres
            self.fiterr_[i] = fiterr

        self.xl_ = self.xc_ - self.r_
        self.xr_ = self.xc_ + self.r_

    def get_yuse(self):
        c = Curve(y = np.nanmean(self.od,axis=1))
        c.removenan()
        # fit TF profile to this
        fitres, fiterr = c.fit(self.fitfun_TF, [c.x.shape[0] / 2, c.x.shape[0] / 4, np.max(c.y), np.max(c.y)/100, np.max(c.y)/100], plot=False)
        fitres[1] = fitres[1] * self.yset_[1]
        self.yuse = np.arange(int(fitres[0]-fitres[1]), int(fitres[0]+fitres[1]), self.yset_[0])
        return self.yuse

    def extend_linear(self):
        fitres = np.polyfit(self.ycen_, self.r_, deg=1)
        self.radfit = np.poly1d(fitres)
        self.rad = self.radfit(self.yall)
        self.area = np.pi * self.rad ** 2

    def extend_poly4(self):
        fitres = np.polyfit(self.ycen_, self.r_, deg=4)
        self.radfit = np.poly1d(fitres)
        self.rad = self.radfit(self.yall)
        self.rad[self.yall < self.ycen_[0]] = self.radfit(self.ycen_[0])
        self.rad[self.yall > self.ycen_[-1]] = self.radfit(self.ycen_[-1])
        self.area = np.pi * self.rad ** 2

    def extend_spline(self):
        tck = spintp.splrep(self.ycen_, self.r_, s=100)
        self.rad = spintp.splev(self.yall, tck, der=0)
        self.rad[self.yall < self.ycen_[0]] = spintp.splev(self.ycen_[0], tck, der=0)
        self.rad[self.yall > self.ycen_[-1]] = spintp.splev(self.ycen_[-1], tck, der=0)
        self.area = np.pi * self.rad ** 2

    def fitfun(self, x, x0, rad, amp, m, b):
        y = 1 - ((x - x0) / rad) ** 2
        y[y <= 0] = 0
        y[y > 0] = np.sqrt(y[y > 0]) * amp
        y += m * x + b
        return y

    def infoplot(self):
        # Figure
        fig = plt.figure(figsize=(8, 5))
        # Setup axes
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
        ax2 = plt.subplot2grid((3, 3), (1, 0), rowspan=2, colspan=2)
        axc = [None] * 3
        axc[0] = plt.subplot2grid((3, 3), (0, 2))
        axc[1] = plt.subplot2grid((3, 3), (1, 2))
        axc[2] = plt.subplot2grid((3, 3), (2, 2))
        # Plot od and measured edges
        ax1.scatter(self.ycen_, self.xl_, s=1, color='white')
        ax1.scatter(self.ycen_, self.xr_, s=1, color='white')
        ax1.scatter(self.ycen_, self.xc_, s=1, color='k')
        ax1.imshow(self.od.T, clim=self.odlim, aspect='auto', cmap='viridis', origin='lower')
        ax1.set(xlim=[self.yall[0], self.yall[-1]], title='OD and radius')
        ax1.set_axis_off()
        # Plot measured and fitted radius
        ax2.plot(self.yall, self.rad, 'k-')
        ax2.scatter(self.ycen_, self.r_, color='red')
        ax2.set(xlim=[self.yall[0], self.yall[-1]])
        # Plot 3 smaple fits
        for i, j in zip([0, 1, 2], [0, self.r_.shape[0] // 2, -1]):
            axc[i].plot(*self.c_[j].xyfitplot, 'k-')
            axc[i].scatter(*self.c_[j].data, color='red', s=1, alpha=0.5)
            axc[i].set_axis_off()
            axc[i].set(title='Cut @ y = {}'.format(self.ycen_[j]))
        # Adjust layout information
        fig.subplots_adjust(hspace=0.1, wspace=-0.1)
        self.fig = fig

    def fitfun_TF(self, x, x0, rad, amp, m=None, b=None):
        y = amp * (1 - ((x - x0) / rad) ** 2) ** (3 / 2)
        y = np.real(y)
        y[np.isnan(y)] = 0
        if m is not None: y += m * x + b
        return y

# Removing OD gradients in cropped image
class ODFix2D:
    def __init__(self, od, cropi, width=20, odlim=(0, 2), plot=False):
        self.prepare(od, cropi, width, odlim)
        self.nanFix()
        self.fit()
        if plot: self.infoplot()

    def prepare(self, od, cropi, width, odlim):
        self.w = width
        self.odlim = odlim
        self.cropi = tuple([slice(x.start - width, x.stop + width, x.step) for x in cropi])
        # Get od and od bg
        self.od_ = od[self.cropi]
        self.odbg = self.od_.copy()
        self.odbg[width:-width, width:-width] = np.nan
        # Generate z = f(x, y), convert grid to 1d
        self.x, self.y = np.meshgrid(np.arange(self.od_.shape[1]), np.arange(self.od_.shape[0]))
        self.z = self.od_[np.isfinite(self.odbg)]
        self.xy = np.array([self.x[np.isfinite(self.odbg)], self.y[np.isfinite(self.odbg)]])

    def nanFix(self):
        # Bad Points
        x, y = np.meshgrid(np.arange(self.od_.shape[1]), np.arange(self.od_.shape[0]))
        self.odx1 = x[np.logical_not(np.isfinite(self.od_))]
        self.ody1 = y[np.logical_not(np.isfinite(self.od_))]
        # Fix OD
        self.od_ = imagedata.fix_od(self.od_, width=5)

    def fit(self):
        from scipy.optimize import curve_fit
        guess = [0, 0, 0]
        self.fitres, self.fiterr = curve_fit(self.fitfun_2DPoly, self.xy, self.z, p0=guess)
        # Plotting items
        self.bg = self.fitfun_2DPoly_2D(self.x, self.y, *self.fitres)
        self.od = self.od_ - self.bg
        self.od = self.od[self.w:-self.w, self.w:-self.w]

    def fitfun_2DPoly(self, xy, b, m1, m2):
        return b + m1 * xy[0] + m2 * xy[1]

    def fitfun_2DPoly_2D(self, x, y, b, m1, m2):
        return b + m1 * x + m2 * y

    def infoplot(self):
        fig = plt.figure(figsize=(8, 5))
        ax = plt.subplot2grid((2, 3), (0, 0), colspan=2)
        ax1 = plt.subplot2grid((2, 3), (0, 2))
        ax2 = plt.subplot2grid((2, 3), (1, 0))
        ax3 = plt.subplot2grid((2, 3), (1, 1))
        ax4 = plt.subplot2grid((2, 3), (1, 2))

        ax.imshow(self.od_.T, clim=self.odlim, cmap='viridis', aspect='auto', origin='lower')
        ax.scatter(self.ody1, self.odx1, color='red', alpha=0.2, marker='.', s=3)
        ax.plot([self.w, self.w, self.od_.shape[0] - self.w, self.od_.shape[0] - self.w, self.w],
                [self.w, self.od_.shape[1] - self.w, self.od_.shape[1] - self.w, self.w, self.w], 'w-')
        ax.set(xlim=[0, self.od_.shape[0]], ylim=[0, self.od_.shape[1]], title='OD: {} points fixed'.format(self.odx1.size))
        ax.set_axis_off()
        ax1.plot(np.nanmean(self.bg[0:self.w, :], axis=0))
        ax1.plot(np.nanmean(self.odbg[0:self.w, :], axis=0), 'r.', markersize=2)
        ax1.set(title='left')
        ax2.plot(np.nanmean(self.bg[:, 0:self.w], axis=1))
        ax2.plot(np.nanmean(self.odbg[:, 0:self.w], axis=1), 'r.', markersize=2)
        ax2.set(title='bottom')
        ax3.plot(np.nanmean(self.bg[:, -self.w:], axis=1))
        ax3.plot(np.nanmean(self.odbg[:, -self.w:], axis=1), 'r.', markersize=2)
        ax3.set(title='top')
        ax4.plot(np.nanmean(self.bg[-self.w:, :], axis=0))
        ax4.plot(np.nanmean(self.odbg[-self.w:, :], axis=0), 'r.', markersize=2)
        ax4.set(title='right')
        self.fig = fig


# Convert OD to Density
class OD2Density:
    def __init__(self, od, xsec, pixel, sigma, nmax=np.inf, Ncor=1, plot=False, center=None):
        self.prepare(od, xsec, pixel, sigma, nmax, Ncor, center)
        self.extract_density_all()
        self.find_center_TF()
        if plot: self.infoplot()

    def prepare(self, od, xsec, pixel, sigma, nmax, Ncor, center):
        self.od = od.copy()
        self.xsec = xsec
        self.pixel = pixel
        self.sigma = sigma
        self.nmax = nmax
        self.Ncor = Ncor
        self.center = center

    def extract_density_all(self):
        atomNumber = np.nansum(self.od, axis=1) * self.pixel ** 2 / self.sigma
        atomDensity = atomNumber / (self.xsec.area * self.pixel ** 3) * self.Ncor
        self.atomDensity = atomDensity

    def find_center_TF(self):
        use = self.atomDensity < self.nmax
        c = Curve(x=np.arange(self.atomDensity.shape[0])[use], y=self.atomDensity[use])
        guess = [c.x.shape[0] / 2, c.x.shape[0] / 4, np.max(c.y), np.max(c.y) / 10, np.max(c.y) / 100]
        fitres, fiterr = c.fit(functions.fitfun_TF_harmonic, guess, plot=False)
        y = c.y - (functions.fitfun_TF_harmonic(c.x, fitres[0], fitres[1], 0, fitres[3], fitres[4]))
        if self.center is None: self.center = fitres[0]
        self.nz = Curve(x=(c.x - self.center) * self.pixel, y=y, xscale=1e-6)
        guess = [self.pixel, fitres[1]*self.pixel, fitres[2], fitres[3], fitres[4]/self.pixel]
        self.nz.fit(functions.fitfun_TF_harmonic, guess, plot=False)

    def infoplot(self):
        fig, ax1 = plt.subplots(figsize=(4, 3))
        ax1.scatter(self.nz.x * 1e6, self.nz.y,color='red',alpha=0.5,marker='.',s=7)
        ax1.plot(self.nz.xyfitplot[0]*1e6,self.nz.xyfitplot[1],'k-')



# Main
def main():
    # # Tests of Curve
    # xi = np.linspace(0,3,100)
    # yi = np.sin(xi**2)
    # dydx = np.cos(xi**2) * 2 * xi
    # yin = yi + np.random.normal(scale=0.1,size=xi.shape)
    # curve0 = Curve(xi,yi)
    # curve1 = Curve(xi, yin)

    # plt.plot(*curve0.plotdata,'b-')
    # plt.plot(*curve1.subsample(bins=4),'r.')
    # plt.plot(xi, dydx,'b-')
    # plt.plot(*curve1.diff(method='poly'),'ko')
    # plt.plot(*curve1.diff(method='gaussian filter'),'gs')
    # plt.show()

    # print(curve0.int())
    # print(curve0.dx)

    wa = np.ones((512, 512));
    woa = np.ones_like(wa) + 0.1;

    img1 = AbsImage(wa=wa, woa=woa)
    print(img1.name)
    img2 = AbsImage(name='03-24-2016_21_04_12_top')
    print(img2.rawdata.shape)
    print(img2)


if __name__ == '__main__':
    main()
