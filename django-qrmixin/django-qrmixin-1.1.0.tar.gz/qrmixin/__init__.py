import os
import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

import qrcode


class QRMixin(object):
    qr_image_field = "qr_image"
    qr_box_size = 2
    qr_border_size = 0
    qr_code_field = "code"

    def get_qr_code(self):
        return getattr(self, self.qr_code_field)

    def generate_qr(self):
        qr_code = self.get_qr_code()
        code_image = qrcode.make(
            qr_code,
            box_size=self.qr_box_size,
            border=self.qr_border_size
        )
        image_field = getattr(self, self.qr_image_field)
        buffer = StringIO.StringIO()
        code_image.save(buffer, "png")
        filename = "qr_{code}.png".format(code=qr_code)
        filename = image_field.field.generate_filename(self, filename)
        filebuffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
        image_field.save(filename, filebuffer)

        return filename