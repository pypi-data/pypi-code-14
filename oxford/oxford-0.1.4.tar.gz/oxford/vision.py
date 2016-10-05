import re

from .base import Base

_analyzeUrl = 'https://api.projectoxford.ai/vision/v1.0/analyze'
_thumbnailUrl = 'https://api.projectoxford.ai/vision/v1.0/generateThumbnail'
_ocrUrl = 'https://api.projectoxford.ai/vision/v1.0/ocr'


class Vision(Base):
    """Client for using the Project Oxford face APIs"""

    def __init__(self, key):
        """Initializes a new instance of the class.
        Args:
            key (str). the API key to use for this client.
        """
        Base.__init__(self, key)

    def analyze(self, options):
        """This operation does a deep analysis on the given image and then extracts a
        set of rich visual features based on the image content.

        Note: exactly one of url, path, or stream must be provided in the options object

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be analyzed
            options.path (string). The Path to image to be analyzed
            options.stream (stream). The stream of the image to be used
            options.ImageType (boolean). The Detects if image is clipart or a line drawing.
            options.Color (boolean). The Determines the accent color, dominant color, if image is black&white.
            options.Faces (boolean). The Detects if faces are present. If present, generate coordinates, gender and age.
            options.Adult (boolean). The Detects if image is pornographic in nature (nudity or sex act). Sexually suggestive content is also detected.
            options.Categories (boolean). The Image categorization; taxonomy defined in documentation.
            options.Tags (boolean). The Image tags; taxonomy defined in documentation.
            options.Description (boolean). The Image description; taxonomy defined in documentation.


        Returns:
            object. The resulting JSON
        """
        flags = []
        params = {}
        for option in options:
            if re.match(r'(Celebrities)', option):
             params['details'] = 'Celebrities'
            elif re.match(r'(ImageType)|(Color)|(Faces)|(Adult)|(Categories)|(Tags)|(Description)', option):
                if options[option]:
                    flags.append(option)
        if flags:
            params['visualFeatures'] = ','.join(flags)

        return Base._postWithOptions(self, _analyzeUrl, options, params)

    def thumbnail(self, options):
        """Generate a thumbnail image to the user-specified width and height. By default, the
        service analyzes the image, identifies the region of interest (ROI), and generates
        smart crop coordinates based on the ROI. Smart cropping is designed to help when you
        specify an aspect ratio that differs from the input image.

        Note: exactly one of url, path, or stream must be provided in the options object

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be thumbnailed
            options.path (string). The Path to image to be thumbnailed
            options.stream (stream). The stream of the image to be used
            options.width (number). The Width of the thumb in pixels
            options.height (number). The Height of the thumb in pixels
            options.smartCropping (boolean). The Should SmartCropping be enabled?

        Returns:
            object. The resulting image binary stream
        """
        params = {
            'width': options['width'] if 'width' in options else 50,
            'height': options['height'] if 'height' in options else 50,
            'smartCropping': options['smartCropping'] if 'smartCropping' in options else False
        }

        return Base._postWithOptions(self, _thumbnailUrl, options, params)

    def ocr(self, options):
        """Optical Character Recognition (OCR) detects text in an image and extracts the recognized
        characters into a machine-usable character stream.

        Note: exactly one of url, path, or stream must be provided in the options object

        Args:
            options (Object). The Options object describing features to extract
            options.url (string). The Url to image to be thumbnailed
            options.path (string). The Path to image to be thumbnailed
            options.stream (stream). The stream of the image to be used
            options.language (string). The BCP-47 language code of the text to be detected in the image. Default value is "unk", then the service will auto detect the language of the text in the image.
            options.detectOrientation (string). The Detect orientation of text in the image

        Returns:
            object. The resulting JSON
        """
        params = {
            'language': options['language'] if 'language' in options else 'unk',
            'detectOrientation': options['detectOrientation'] if 'detectOrientation' in options else True
        }

        return Base._postWithOptions(self, _ocrUrl, options, params)
