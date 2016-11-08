#
# FITSImage.py -- Abstraction of a FITS data image.
#
# Eric Jeschke (eric@naoj.org)
#
# Copyright (c)  Eric R. Jeschke.  All rights reserved.
# This is open-source software licensed under a BSD license.
# Please see the file LICENSE.txt for details.
#
from ginga.util import wcsmod, io_fits
from ginga.util import wcs, iqcalc
from ginga.AstroImage import AstroImage, ImageError, Header


class FITSHeader(Header):
    pass

class FITSImage(AstroImage):
    """
    Abstraction of a FITS data (image).
    """

    def __init__(self, data_np=None, metadata=None, logger=None,
                 wcsclass=wcsClass, ioclass=ioClass,
                 inherit_primary_header=False):

        AstroImage.__init__(self, data_np=None, metadata=None, logger=None,
                            wcsclass=wcsClass, ioclass=ioClass)

        # wcsclass specifies a pluggable WCS module
        if wcsclass is None:
            wcsclass = wcsmod.WCS
        self.wcs = wcsclass(self.logger)

        # wcsclass specifies a pluggable IO module
        if ioclass is None:
            ioclass = io_fits.fitsLoaderClass
        self.io = ioclass(self.logger)

        self.inherit_primary_header = inherit_primary_header

        if self.inherit_primary_header:
            self._primary_hdr = AstroHeader()
        else:
            self._primary_hdr = None

        if metadata is not None:
            header = self.get_header()
            self.wcs.load_header(header)

        self.naxispath = []
        self.revnaxis = []

    def load_hdu(self, hdu, fobj=None, naxispath=None):
        self.clear_metadata()

        ahdr = self.get_header()

        loader = io_fits.PyFitsFileHandler(self.logger)
        data, naxispath = loader.load_hdu(hdu, ahdr, naxispath=naxispath)
        if naxispath is None:
            naxispath = []
        self.naxispath = naxispath
        self.revnaxis = list(naxispath)
        self.revnaxis.reverse()

        # Set PRIMARY header
        if self.inherit_primary_header and fobj is not None:
            self.io.fromHDU(fobj[0], self._primary_hdr)

        self.set_data(data)

        # Try to make a wcs object on the header
        self.wcs.load_header(hdu.header, fobj=fobj)

    def load_file(self, filepath, numhdu=None, naxispath=None):
        self.logger.debug("Loading file '%s' ..." % (filepath))
        self.clear_metadata()

        ahdr = self.get_header()

        # User specified an HDU using bracket notation at end of path?
        match = re.match(r'^(.+)\[(\d+)\]$', filepath)
        if match:
            filepath = match.group(1)
            numhdu = max(int(match.group(2)), 0)

        data, numhdu, naxispath = self.io.load_file(filepath, ahdr,
                                                    numhdu=numhdu,
                                                    naxispath=naxispath,
                                                    phdr=self._primary_hdr)

        if naxispath is None:
            naxispath = []
        self.naxispath = naxispath
        self.revnaxis = list(naxispath)
        self.revnaxis.reverse()

        # Set the name to the filename (minus extension) if no name
        # currently exists for this image
        name = self.get('name', None)
        if name is None:
            dirpath, filename = os.path.split(filepath)
            name, ext = os.path.splitext(filename)
            # Remove trailing .extension
            if '.' in name:
                name = name[:name.rindex('.')]
            if numhdu is not None:
                name += ('[%d]' % numhdu)
            self.set(name=name)

        self.set(path=filepath, idx=numhdu)

        self.set_data(data)

        # Try to make a wcs object on the header
        # TODO: in order to do more sophisticated WCS (e.g. distortion
        #   correction) that requires info in additional headers we need
        #   to pass additional information to the wcs class
        #self.wcs.load_header(hdu.header, fobj=fobj)
        self.wcs.load_header(ahdr)

#END
