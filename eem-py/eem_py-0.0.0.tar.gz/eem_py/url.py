import base64
import six

from .signature import Signature


def signed_url(key, host, source, **kwargs):
    ops = []

    debug = kwargs.pop('debug', False)

    # sort operations by lowercase, this improves the consistency of
    # signature generation for a given source image
    for operation, params in sorted(kwargs.items(), key=lambda x: x[0].lower()):
        if isinstance(params, bool):
            # we only need the 'operation' in the final `ops`
            params = ''
        elif isinstance(params, six.string_types):
            params = ','.join([p.strip() for p in params.split(',')])
        elif isinstance(params, six.integer_types):
            params = six.text_type(params)
        else:
            continue

        ops.append(('{operation}({params})' if params else '{operation}').format(
            operation=operation.lower(),
            params=params
        ))

    operations = ';'.join(ops) or 'original'

    parts = [operations, source]
    signature = Signature.generate_with_key('/'.join(parts), key)

    return '{host}/{signature}/{operations}/{source}'.format(
        host=host.rstrip('/'),
        source=source,
        signature=signature,
        operations=six.text_type(base64.urlsafe_b64encode(
            bytes(operations.encode('utf-8'))
        ), 'ascii').rstrip('=') if not debug else operations
    )
