from ginga import AstroImage, RGBImage
from ginga.util.wcsmod import AstropyWCS
from ginga.util import io_rgb

try:
    from pyavm import AVM
    have_pyavm = True

except ImportError:
    have_pyavm = False


class RGBAstroImage(RGBImage.RGBImage, AstroImage.AstroImage):

    def __init__(self, data_np=None, metadata=None,
                 logger=None, order='RGBA',
                 ioclass=io_rgb.RGBFileHandler):

        AstroImage.AstroImage.__init__(self, logger=logger)
        RGBImage.RGBImage.__init__(self, data_np=data_np, metadata=metadata,
                                   logger=self.logger)

    def load_file(self, filepath):
        kwds = AstroImage.AstroHeader()
        metadata = { 'header': kwds, 'path': filepath }

        # TODO: ideally we would be informed by channel order
        # in result by io_rgb
        data_np = self.io.load_file(filepath, kwds)

        self.set_data(data_np, metadata=metadata)

        if have_pyavm:
            try:
                avm = AVM.from_image(filepath)

                print("making wcs")
                self.wcs = AstropyWCS(self.logger)
                self.wcs.wcs = avm.to_wcs()
                print(("wcs is", wcs))

            except Exception as e:
                self.logger.warning("Error reading AVM data from image: %s" % (
                    str(e)))
                return

            # other things we need to override
            self.naxispath = []
            self.revnaxis = []
