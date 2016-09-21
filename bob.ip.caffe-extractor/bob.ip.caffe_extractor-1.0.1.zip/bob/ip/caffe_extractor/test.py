import caffe
import bob.io.base
import bob.ip.caffe_extractor
import pkg_resources
import numpy
import os


def test_vgg():

    file_name = os.path.join(pkg_resources.resource_filename(__name__, 'data'), '8821.hdf5')
    reference_file_name = os.path.join(pkg_resources.resource_filename(__name__, 'data'), 'reference.hdf5')
    reference = bob.io.base.load(reference_file_name)

    f = bob.io.base.load(file_name)

    extractor = bob.ip.caffe_extractor.VGGFace("fc7")
    feature = extractor(f)

    assert numpy.any(numpy.isclose(feature, reference,rtol=1e-08, atol=1e-08))
