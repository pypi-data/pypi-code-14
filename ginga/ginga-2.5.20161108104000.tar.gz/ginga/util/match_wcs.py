from ginga.util.six.moves import map, zip

class WcsMatch(object):
    """
    CREDIT: Code modified from
      http://www.astropython.org/snippet/2011/1/Fix-the-WCS-for-a-FITS-image-file
    """
    def __init__(self, header, wcsClass, xy_coords, ref_coords):
        # Image 
        self.hdr = header
        from ginga.misc.log import NullLogger
        self.wcs = wcsClass(NullLogger())
        self.wcs.load_header(self.hdr)

        # Reference (correct) source positions in RA, Dec
        self.ref_coords = numpy.array(ref_coords)

        # Get source pixel positions from reference coords
        #xy_coords = map(lambda args: self.wcs.radectopix(*args), img_coords)
        self.pix0 = numpy.array(xy_coords).flatten()

        # Copy the original WCS CRVAL and CD values
        self.has_cd = False
        self.crval = numpy.array(self.wcs.get_keywords('CRVAL1', 'CRVAL2'))
        try:
            cd = numpy.array(self.wcs.get_keywords('CD1_1', 'CD1_2',
                                                   'CD2_1', 'CD2_2'))
            self.cd = cd.reshape((2, 2))
            self.has_cd = True
        except KeyError:
            cd = numpy.array(self.wcs.get_keywords('PC1_1', 'PC1_2',
                                                   'PC2_1', 'PC2_2'))
            self.cd = cd.reshape((2, 2))

    def rotate(self, degs):
        rads = numpy.radians(degs)
        s = numpy.sin(rads)
        c = numpy.cos(rads)
        return numpy.array([[c, -s],
                            [s, c]])

    def calc_pix(self, pars):
        """For the given d_ra, d_dec, and d_theta pars, update the WCS
        transformation and calculate the new pixel coordinates for each
        reference source position.
        """
        # calculate updated ra/dec and rotation
        d_ra, d_dec, d_theta = pars
        crval = self.crval + numpy.array([d_ra, d_dec]) / 3600.0
        cd = numpy.dot(self.rotate(d_theta), self.cd)

        # temporarily assign to the WCS
        d = self.hdr
        d.update(dict(CRVAL1=crval[0], CRVAL2=crval[1]))
        if self.has_cd:
            d.update(dict(CD1_1=cd[0,0], CD1_2=cd[0,1], CD2_1=cd[1,0], CD2_2=cd[1,1]))
        else:
            d.update(dict(PC1_1=cd[0,0], PC1_2=cd[0,1], PC2_1=cd[1,0], PC2_2=cd[1,1]))
        self.wcs.load_header(self.hdr)

        # calculate the new pixel values based on this wcs
        pix = numpy.array(map(lambda args: self.wcs.radectopix(*args),
                              self.ref_coords)).flatten()

        #print 'pix =', pix
        #print 'pix0 =', self.pix0
        return pix

    def calc_resid2(self, pars):
        """Return the squared sum of the residual difference between the
        original pixel coordinates and the new pixel coords (given offset
        specified in ``pars``)
        
        This gets called by the scipy.optimize.fmin function.
        """
        pix = self.calc_pix(pars)
        resid2 = numpy.sum((self.pix0 - pix) ** 2) # assumes uniform errors
        #print 'resid2 =', resid2
        return resid2

    def calc_match(self):
        from scipy.optimize import fmin
        x0 = numpy.array([0.0, 0.0, 0.0])

        d_ra, d_dec, d_theta = fmin(self.calc_resid2, x0)

        crval = self.crval + numpy.array([d_ra, d_dec]) / 3600.0
        cd = numpy.dot(self.rotate(d_theta), self.cd)

        d = self.hdr
        d.update(dict(CRVAL1=crval[0], CRVAL2=crval[1]))
        if self.has_cd:
            d.update(dict(CD1_1=cd[0,0], CD1_2=cd[0,1], CD2_1=cd[1,0], CD2_2=cd[1,1]))
        else:
            d.update(dict(PC1_1=cd[0,0], PC1_2=cd[0,1], PC2_1=cd[1,0], PC2_2=cd[1,1]))
        self.wcs.load_header(self.hdr)
        
        # return delta ra/dec and delta rotation
        return (d_ra, d_dec, d_theta)

def match_wcs(image, img_coords, ref_coords):
    """Adjust WCS (CRVAL{1,2} and CD{1,2}_{1,2}) using a rotation
    and linear offset so that ``img_coords`` matches ``ref_coords``.

    Parameters
    ----------
    img_coords: seq like
        list of (ra, dec) coords in input image
    ref_coords: seq like
        list of reference coords to match
    """
    header = image.get_header()
    wcsClass = image.wcs.__class__
    wcs_m = wcs.WcsMatch(header, wcsClass, img_coords, ref_coords)
    res = wcs_m.calc_match()
    return wcs_m, res
        
