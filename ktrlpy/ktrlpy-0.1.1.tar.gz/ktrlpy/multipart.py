import random
import mimetypes


def encode_multipart_formdata(fields, files):
    '''
    encode the given field and files into a multipart request body

    Args:
        fields (dict): a dict of regular form fields
        files (dict): a dict of format name: (filename, value)
    Returns:
        tuple of (content_type, body) for use in making http requests
    '''
    BOUNDARY = '----------{:022d}'.format(
        random.randint(0, 10000000000000000000000))
    CRLF = '\r\n'
    lines = []
    for key, value in fields.iteritems():
        lines.append("--" + BOUNDARY)
        lines.append('Content-Disposition: form-data; name="{}"'.format(key))
        lines.append('')
        lines.append(value)
    for key, (filename, value) in files.iteritems():
        lines.append("--" + BOUNDARY)
        lines.append(
            'Content-Disposition: form-data; name="{}"; filename="{}"'.format(
                key, filename))
        lines.append('Content-Type: {}'.format(get_content_type(filename)))
        lines.append("")
        lines.append(value)
    lines.append("--" + BOUNDARY + "--")
    lines.append("")
    body = CRLF.join(lines)
    content_type = 'multipart/form-data; boundary={}'.format(BOUNDARY)
    return content_type, body


def get_content_type(filename):
    '''
    returns a valid mime-type for file with the the given name
    '''
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
