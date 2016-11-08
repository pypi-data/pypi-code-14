from ginga.util import io_fits
io_fits.use('fitsio')
#io_fits.use('astropy')

from ginga.misc.log import get_logger
logger = get_logger(log_stderr=True, level=10)

from ginga import AstroImage

#path = "/home/eric/testdata/HST/iaby02x7q_flt.fits[DQ,1]"
path = "/home/eric/testdata/HST/iaby02x7q_flt.fits[DQ,2]"
#path = "/home/eric/testdata/HST/iaby02x7q_flt.fits[DQ]"
#path = "/home/eric/testdata/HST/iaby02x7q_flt.fits[PRIMARY]"
#path = "/home/eric/testdata/HST/iaby02x7q_flt.fits[3]"
foo = AstroImage.AstroImage(logger=logger)

foo.load_file(path)
print("Name is '%s'" % (foo.get('name')))
