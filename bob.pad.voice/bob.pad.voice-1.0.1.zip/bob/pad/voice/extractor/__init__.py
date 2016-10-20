from .lbps import LBPs
from .ratios import Ratios
from .vectors_ratios import VectorsRatios
from .glcms import GLCMs
from .spectrogram_extended import SpectrogramExtended
from .lbp_histograms import LBPHistograms

# to fix sphinx warnings of not able to find classes, when path is shortened
Ratios.__module__ = "bob.pad.voice.extractor"
LBPs.__module__ = "bob.pad.voice.extractor"
VectorsRatios.__module__ = "bob.pad.voice.extractor"
GLCMs.__module__ = "bob.pad.voice.extractor"
SpectrogramExtended.__module__ = "bob.pad.voice.extractor"
LBPHistograms.__module__ = "bob.pad.voice.extractor"
# gets sphinx autodoc done right - don't remove it
__all__ = [_ for _ in dir() if not _.startswith('_')]
