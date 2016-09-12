# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Model a fiber spectrograph camera for spectroscopic simulations.

Cameras belong to an :class:`Instrument <specsim.instrument.Instrument>` and
are usually initialized from a configuration used to create
a simulator and then accessible via its ``instrument.cameras`` attribute,
for example:

    >>> import specsim.simulator
    >>> simulator = specsim.simulator.Simulator('test')
    >>> print(np.round(simulator.instrument.cameras[0].read_noise, 1))
    2.9 electron / pix2

See :doc:`/api` for examples of changing model parameters defined in the
configuration. No attributes can be changed after a simulator has
been created.  File a github issue if you would like to change this.
"""
from __future__ import print_function, division

import numpy as np
import scipy.sparse

import astropy.units as u


class Camera(object):
    """Model the response of a single fiber spectrograph camera.

    No camera attributes can be changed after an instrument has been
    created.  File a github issue if you would like to change this.

    Parameters
    ----------
    name : str
        A brief descriptive name for this camera.  Typically a single letter
        indicating the wavelength band covered by this camera.
    wavelength : astropy.units.Quantity
        Array of wavelength bin centers where the instrument response is
        calculated, with units.  Must be equally spaced.
    throughput : numpy.ndarray
        Array of throughput values tabulated at each wavelength bin center.
    row_size : astropy.units.Quantity
        Array of row size values tabulated at each wavelength bin center.
        Units are required, e.g. Angstrom / pixel.
    fwhm_resolution : astropy.units.Quantity
        Array of wavelength resolution FWHM values tabulated at each wavelength
        bin center. Units are required, e.g., Angstrom.
    neff_spatial : astropy.units.Quantity
        Array of effective trace sizes in the spatial (fiber) direction
        tabulated at each wavelength bin center.  Units are required, e.g.
        pixel.
    read_noise : astropy.units.Quantity
        Camera noise per readout operation.  Units are required, e.g. electron.
    dark_current : astropy.units.Quantity
        Nominal mean dark current from sensor.  Units are required, e.g.
        electron / hour.
    gain : astropy.units.Quantity
        CCD amplifier gain.  Units are required, e.g., electron / adu.
        (This is really 1/gain).
    num_sigmas_clip : float
        Number of sigmas where the resolution should be clipped when building
        a sparse resolution matrix.
    output_pixel_size : astropy.units.Quantity
        Size of output pixels for this camera.  Units are required, e.g.
        Angstrom. Must be a multiple of the the spacing of the wavelength
        input parameter.
    """
    def __init__(self, name, wavelength, throughput, row_size,
                 fwhm_resolution, neff_spatial, read_noise, dark_current,
                 gain, num_sigmas_clip, output_pixel_size):
        self.name = name
        self._wavelength = wavelength.to(self._wavelength_unit).value
        self.throughput = throughput
        self._row_size = row_size.to(self._wavelength_unit / u.pixel).value
        self._fwhm_resolution = fwhm_resolution.to(self._wavelength_unit).value
        self._neff_spatial = neff_spatial.to(u.pixel).value
        self.read_noise = read_noise
        self.dark_current = dark_current
        self.gain = gain
        self.num_sigmas_clip = num_sigmas_clip

        # The arrays defining the CCD properties must all have identical
        # wavelength coverage.
        ccd_nonzero = np.where(self._row_size > 0)[0]
        ccd_start, ccd_stop = ccd_nonzero[0], ccd_nonzero[-1] + 1
        if (np.any(self._fwhm_resolution[:ccd_start] != 0) or
            np.any(self._fwhm_resolution[ccd_stop:] != 0)):
            raise RuntimeError('Resolution extends beyond CCD coverage.')
        if (np.any(self._neff_spatial[:ccd_start] != 0) or
            np.any(self._neff_spatial[ccd_stop:] != 0)):
            raise RuntimeError('Spatial Neff extends beyond CCD coverage.')

        # CCD properties must be valid across the coverage.
        if np.any(self._row_size[ccd_start:ccd_stop] <= 0.):
            raise RuntimeError('CCD row size has invalid values <= 0.')
        if np.any(self._fwhm_resolution[ccd_start:ccd_stop] <= 0.):
            raise RuntimeError('CCD resolution has invalid values <= 0.')
        if np.any(self._neff_spatial[ccd_start:ccd_stop] <= 0.):
            raise RuntimeError('CCD spatial Neff has invalid values <= 0.')

        self.ccd_slice = slice(ccd_start, ccd_stop)
        self.ccd_coverage = np.zeros_like(self._wavelength, dtype=bool)
        self.ccd_coverage[ccd_start:ccd_stop] = True
        self._wavelength_min = self._wavelength[ccd_start]
        self._wavelength_max = self._wavelength[ccd_stop - 1]

        # Calculate the size of each wavelength bin in units of pixel rows.
        self._wavelength_bin_size = np.gradient(self._wavelength)
        neff_wavelength = np.zeros_like(self._neff_spatial)
        neff_wavelength[self.ccd_slice] = (
            self._wavelength_bin_size[self.ccd_slice] /
            self._row_size[self.ccd_slice])

        # Calculate the effective pixel area contributing to the signal
        # in each wavelength bin.
        self.neff_pixels = neff_wavelength * self._neff_spatial * u.pixel ** 2

        # Calculate the read noise per wavelength bin, assuming that
        # readnoise is uncorrelated between pixels (hence the sqrt scaling). The
        # value will be zero in pixels that are not used by this camera.
        self.read_noise_per_bin = (
            self.read_noise * np.sqrt(self.neff_pixels.value) * u.pixel ** 2
            ).to(u.electron)

        # Calculate the dark current per wavelength bin.
        self.dark_current_per_bin = (
            self.dark_current * self.neff_pixels).to(u.electron / u.s)

        # Calculate the RMS resolution assuming a Gaussian PSF.
        fwhm_to_sigma = 1. / (2 * np.sqrt(2 * np.log(2)))
        self._rms_resolution = fwhm_to_sigma * self._fwhm_resolution

        # Find the minimum wavelength that can disperse into the CCD,
        # assuming a constant extrapolation of the resolution.
        sigma_lo = self._rms_resolution[ccd_start]
        min_wave = (self._wavelength[ccd_start] -
                    self.num_sigmas_clip * sigma_lo)
        if min_wave < self._wavelength[0]:
            raise RuntimeError(
                'Wavelength grid min does not cover {0}-camera response.'
                .format(self.name))
        matrix_start = np.where(self._wavelength >= min_wave)[0][0]

        # Find the maximum wavelength that can disperse into the CCD,
        # assuming a constant extrapolation of the resolution.
        sigma_hi = self._rms_resolution[ccd_stop - 1]
        max_wave = (self._wavelength[ccd_stop - 1] +
                    self.num_sigmas_clip * sigma_hi)
        if max_wave > self._wavelength[-1]:
            raise RuntimeError(
                'Wavelength grid max does not cover {0}-camera response.'
                .format(self.name))
        matrix_stop = np.where(self._wavelength <= max_wave)[0][-1] + 1
        self.response_slice = slice(matrix_start, matrix_stop)

        # Pad the RMS array to cover the full resolution matrix range.
        sigma = np.empty((matrix_stop - matrix_start))
        sigma[:ccd_start - matrix_start] = sigma_lo
        sigma[ccd_start - matrix_start:ccd_stop - matrix_start] = (
            self._rms_resolution[ccd_start:ccd_stop])
        sigma[ccd_stop - matrix_start:] = sigma_hi

        # Calculate the range of wavelengths where the dispersion will
        # be evaluated.  The evaluation range extends beyond wavelengths that
        # can disperse into the CCD in order to calculate the normalization.
        wave = self._wavelength[matrix_start:matrix_stop]
        min_wave = wave - self.num_sigmas_clip * sigma
        max_wave = wave + self.num_sigmas_clip * sigma
        eval_start = np.searchsorted(self._wavelength, min_wave)
        eval_stop = np.searchsorted(self._wavelength, max_wave) + 1

        # The columns of the resolution matrix are clipped to the CCD coverage.
        column_start = np.maximum(eval_start, ccd_start)
        column_stop = np.minimum(eval_stop, ccd_stop)
        column_size = column_stop - column_start
        assert np.all(column_size > 0)

        # Prepare start, stop values for slicing eval -> column.
        trim_start = column_start - eval_start
        trim_stop = column_stop - eval_start
        assert np.all(trim_stop > trim_start)

        # Prepare a sparse resolution matrix in compressed column format.
        matrix_size = np.sum(column_size)
        data = np.empty((matrix_size,), float)
        indices = np.empty((matrix_size,), int)
        indptr = np.empty((len(column_size) + 1,), int)
        indptr[0] = 0
        indptr[1:] = np.cumsum(column_size)
        assert indptr[-1] == matrix_size

        # Fill sparse matrix arrays.
        sparse_start = 0
        for i in range(matrix_stop - matrix_start):
            eval_slice = slice(eval_start[i], eval_stop[i])
            w = self._wavelength[eval_slice]
            dw = self._wavelength_bin_size[eval_slice]
            column = dw * np.exp(-0.5 * ((w - wave[i]) / sigma[i]) ** 2)
            # Normalize over the full evaluation range.
            column /= np.sum(column)
            # Trim to the CCD coverage.
            s = slice(sparse_start, sparse_start + column_size[i])
            data[s] = column[trim_start[i]:trim_stop[i]]
            indices[s] = np.arange(column_start[i], column_stop[i]) - ccd_start
            sparse_start = s.stop
        assert np.all((indices >= 0) & (indices < ccd_stop - ccd_start))
        assert s.stop == matrix_size

        # Create the matrix in CSC format.
        matrix_shape = (ccd_stop - ccd_start, matrix_stop - matrix_start)
        self._resolution_matrix = scipy.sparse.csc_matrix(
            (data, indices, indptr), shape=matrix_shape)
        # Convert to CSR format for faster matrix multiplies.
        self._resolution_matrix = self._resolution_matrix.tocsr()

        # Initialize downsampled output pixels.
        self._output_pixel_size = (
            output_pixel_size.to(self._wavelength_unit).value)
        # Check that we can downsample simulation pixels to obtain
        # output pixels.  This check will only work if the simulation
        # grid is equally spaced, but no other part of the Camera class
        # class currently requires this.
        wavelength_step = self._wavelength[1] - self._wavelength[0]
        self._downsampling = int(round(
            self._output_pixel_size / wavelength_step))
        num_downsampled = int(
            (self._wavelength_max - self._wavelength_min) //
            self._output_pixel_size)
        pixel_edges = (
            self._wavelength_min - 0.5 * wavelength_step +
            np.arange(num_downsampled + 1) * self._output_pixel_size)
        sim_edges = (
            self._wavelength[self.ccd_slice][::self._downsampling] -
             0.5 * wavelength_step)
        if not np.allclose(
            pixel_edges, sim_edges, rtol=0., atol=1e-6 * wavelength_step):
            raise ValueError(
                'Cannot downsample {0}-camera pixels from {1:f} to {2} {3}.'
                .format(self.name, wavelength_step, self._output_pixel_size,
                        self._wavelength_unit))
        # Save the centers of each output pixel.
        self._output_wavelength = 0.5 * (pixel_edges[1:] + pixel_edges[:-1])
        # Initialize the parameters used by the downsample() method.
        self._output_slice = slice(
            self.ccd_slice.start,
            self.ccd_slice.start + num_downsampled * self._downsampling)
        self._downsampled_shape = (num_downsampled, self._downsampling)


    def get_output_resolution_matrix(self):
        """Return the output resolution matrix.

        The output resolution is calculated by summing output pixel
        blocks of the full resolution matrix.  This is equivalent to
        the convolution of our resolution with a boxcar representing
        an output pixel.

        This operation is relatively slow and requires a lot of memory
        since the full resolution matrix is expanded to a dense array
        during the calculation.

        The result is returned as a dense matrix but will generally be
        sparse, so can be converted to one of the scipy.sparse formats.
        The result is not saved internally.

        Edge effects are not handled very gracefully in order to return
        a square matrix.

        Returns
        -------
        numpy.ndarray
            Square array of resolution matrix elements.
        """
        n = len(self._output_wavelength)
        m = self._downsampling
        i0 = self.ccd_slice.start - self.response_slice.start
        return (self._resolution_matrix[: n * m, i0 : i0 + n * m].toarray()
                .reshape(n, m, n, m).sum(axis=3).sum(axis=1) / float(m))


    def downsample(self, data, method=np.sum):
        """Downsample data tabulated on the simulation grid to output pixels.
        """
        data = np.asanyarray(data)
        if data.shape != self._wavelength.shape:
            raise ValueError(
                'Invalid data shape for downsampling: {0}.'.format(data.shape))

        return method(
            data[self._output_slice].reshape(self._downsampled_shape), axis=-1)


    def apply_resolution(self, flux):
        """
        Input should be on the simulation wavelength grid.

        Any throughput should already be applied.
        """
        flux = np.asarray(flux)
        dispersed = np.zeros_like(flux)

        dispersed[self.ccd_slice] = self._resolution_matrix.dot(
            flux[self.response_slice])

        return dispersed


    # Canonical wavelength unit used for all internal arrays.
    _wavelength_unit = u.Angstrom


    @property
    def wavelength_min(self):
        """Minimum wavelength covered by this camera's CCD.
        """
        return self._wavelength_min * self._wavelength_unit


    @property
    def wavelength_max(self):
        """Maximum wavelength covered by this camera's CCD.
        """
        return self._wavelength_max * self._wavelength_unit


    @property
    def rms_resolution(self):
        """Array of RMS resolution values.
        """
        return self._rms_resolution * self._wavelength_unit


    @property
    def row_size(self):
        """Array of row sizes in the dispersion direction.
        """
        return self._row_size * self._wavelength_unit / u.pixel


    @property
    def neff_spatial(self):
        """Array of effective pixel dimensions in the spatial (fiber) direction.
        """
        return self._neff_spatial * u.pixel


    @property
    def output_pixel_size(self):
        """Size of output pixels.

        Must be a multiple of the simulation wavelength grid.
        """
        return self._output_pixel_size * self._wavelength_unit


    @property
    def output_wavelength(self):
        """Output pixel central wavelengths.
        """
        return self._output_wavelength * self._wavelength_unit
