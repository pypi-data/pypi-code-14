import argparse
import getpass
import hashlib
import json
import socket
import sys

from . import doc_split, usage, version
from .transfer_client import TransferClient


def _write(output_handle, data):
    output_handle.write('{}\n'.format(json.dumps(data, indent=4)))


def users(output_handle, server_name, user_id, ssl_check):
    """
    Gives a JSON object of a user together with its transfers.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle, TransferClient(server_name, ssl_check).users(user_id))


def schema(output_handle, server_name, user_id, ssl_check):
    """
    Gives the JSON schema for a user.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle, TransferClient(server_name, ssl_check).schema(user_id))


def transfers(output_handle, metadata_handle, server_name, user_id, ssl_check):
    """
    Initiates a new transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg stream metadata_handle: Open readable handle to a metadata file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).transfers(
        user_id, json.loads(metadata_handle.read())))


def status(output_handle, server_name, user_id, transfer_id, ssl_check):
    """
    Gives a JSON object of a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).status(
        user_id, transfer_id))


def update(
        output_handle, server_name, user_id, transfer_id, status, ssl_check):
    """
    Updates a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg str status: Transfer status.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).update(
        user_id, transfer_id, status))


def uploads(
        output_handle, file_handle, server_name, user_id, transfer_id,
        ssl_check):
    """
    Uploads a file to a transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg stream file_handle: Open readable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str transfer_id: Transfer ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(output_handle, TransferClient(server_name, ssl_check).uploads(
        user_id, transfer_id, file_handle))


def completed(output_handle, server_name, client_id, ssl_check):
    """
    Gives a JSON object of all transfers for this client, i.e., a list of
    transfer ids.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str client_id: Client ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    _write(
        output_handle,
        TransferClient(server_name, ssl_check).completed(client_id))


def _make_metadata(file_handles, title):
    """
    Given a list of files, generate the metadata according to the minimal
    transfer metadata schema.

    :arg list file_handles: List of open readable file handles.
    :arg str title: Transfer title.

    :returns dict: Metadata in JSON format.
    """
    metadata = {'title': title, 'files': []}

    for file_handle in file_handles:
        hash_sum = hashlib.md5()
        for chunk in iter(lambda: file_handle.read(4096), b''):
            hash_sum.update(chunk)
        file_handle.seek(0)

        metadata['files'].append({
            'filename': file_handle.name,
            'md5': hash_sum.hexdigest()})

    return metadata


def make_metadata(output_handle, file_handles, title):
    """
    Given a list of files, generate the metadata according to the minimal
    transfer metadata schema.

    :arg stream output_handle: Open writeable handle to a file.
    :arg list file_handles: List of open readable file handles.
    :arg str title: Transfer title.
    """
    _write(output_handle, _make_metadata(file_handles, title))


def transfer(
        output_handle, file_handles, server_name, user_id, title, ssl_check):
    """
    Transfer a list of files.

    :arg stream output_handle: Open writeable handle to a file.
    :arg list file_handles: List of open readable file handles.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg str title: Transfer title.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfer_id = transfer_client.transfers(
        user_id, _make_metadata(file_handles, title))['id']
    output_handle.write('Transfer ID: {}.\n'.format(transfer_id))
    for file_handle in file_handles:
        output_handle.write('Uploading file: {}.\n'.format(file_handle.name))
        transfer_client.uploads(user_id, transfer_id, file_handle)


def _interrupted_transfer(output_handle, transfer_client, user_id):
    """
    Find an interrupted transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg object transfer_client: Transfer client class instance.
    :arg str user_id: User ID.

    :returns dict: Interrupted transfer object in JSON format.
    """
    transfers = transfer_client.users(user_id)['transfers']

    if not (transfers and transfers[-1]['status'] == 'initiated'):
        raise ValueError('no interrupted transfers found')

    transfer = transfers[-1]
    output_handle.write('Transfer ID: {}.\n'.format(transfer['id']))

    return transfer


def resume(output_handle, server_name, user_id, ssl_check):
    """
    Resume an interrupted transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfer = _interrupted_transfer(output_handle, transfer_client, user_id)
    for file_object in transfer['files']:
        if file_object['status'] == 'pending':
            output_handle.write(
                'Uploading file: {}.\n'.format(file_object['filename']))
            with open(file_object['filename'], 'rb') as file_handle:
                transfer_client.uploads(user_id, transfer['id'], file_handle)


def cancel(output_handle, server_name, user_id, ssl_check):
    """
    Cancel an interrupted transfer.

    :arg stream output_handle: Open writeable handle to a file.
    :arg str server_name: Name of the transfer server.
    :arg str user_id: User ID.
    :arg bool ssl_check: Check server SSL certificate.
    """
    transfer_client = TransferClient(server_name, ssl_check)

    transfer = _interrupted_transfer(output_handle, transfer_client, user_id)
    transfer_client.update(user_id, transfer['id'], 'cancelled')


def main():
    """
    Main entry point.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage[0], epilog=usage[1])
    parser.add_argument('-v', action='version', version=version(parser.prog))
    subparsers = parser.add_subparsers(dest='subcommand')

    server_name_parser = argparse.ArgumentParser(add_help=False)
    server_name_parser.add_argument(
        'server_name', metavar='SERVER', type=str, help='server name')

    user_id_parser = argparse.ArgumentParser(add_help=False)
    user_id_parser.add_argument(
        'user_id', metavar='USER', type=str, help='user id')

    transfer_id_parser = argparse.ArgumentParser(add_help=False)
    transfer_id_parser.add_argument(
        'transfer_id', metavar='TRANSFER', type=str, help='transfer id')

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '-o', dest='output_handle', metavar='OUTPUT',
        type=argparse.FileType('w'), default=sys.stdout, help='output file')

    files_parser = argparse.ArgumentParser(add_help=False)
    files_parser.add_argument(
        'file_handles', metavar='FILE', type=argparse.FileType('rb'),
        nargs='+', help='files to be transferred')

    title_parser = argparse.ArgumentParser(add_help=False)
    title_parser.add_argument(
        '-t', dest='title', type=str,
        default='Transfer from {} by {} using {}'.format(
            socket.gethostname(), getpass.getuser(), parser.prog),
        help='transfer title (default="%(default)s")')

    ssl_parser = argparse.ArgumentParser(add_help=False)
    ssl_parser.add_argument(
        '-n', dest='ssl_check', default=True, action='store_false',
        help='disable ssl certificate check')

    default_parser = argparse.ArgumentParser(
        add_help=False,
        parents=[output_parser, server_name_parser, user_id_parser,
            ssl_parser])

    subparser = subparsers.add_parser(
        'users', parents=[default_parser],
        description=doc_split(users))
    subparser.set_defaults(func=users)

    subparser = subparsers.add_parser(
        'schema', parents=[default_parser],
        description=doc_split(schema))
    subparser.set_defaults(func=schema)

    subparser = subparsers.add_parser(
        'transfers',
        parents=[default_parser],
        description=doc_split(transfers))
    subparser.add_argument(
        'metadata_handle', metavar='METADATA', type=argparse.FileType('r'),
        help='metadata file')
    subparser.set_defaults(func=transfers)

    subparser = subparsers.add_parser(
        'status', parents=[default_parser, transfer_id_parser],
        description=doc_split(status))
    subparser.set_defaults(func=status)

    subparser = subparsers.add_parser(
        'update', parents=[default_parser, transfer_id_parser],
        description=doc_split(update))
    subparser.add_argument(
        'status', metavar='STATUS', choices=['cancelled'],
        help='transfer status (choose from: {%(choices)s})')
    subparser.set_defaults(func=update)

    subparser = subparsers.add_parser(
        'uploads',
        parents=[default_parser, transfer_id_parser],
        description=doc_split(uploads))
    subparser.add_argument(
        'file_handle', metavar='FILE', type=argparse.FileType('rb'),
        help='file to be transferred')
    subparser.set_defaults(func=uploads)

    subparser = subparsers.add_parser(
        'completed', parents=[output_parser, server_name_parser],
        description=doc_split(completed))
    subparser.add_argument('client_id', metavar='CLIENT',
        type=str, help='client id')
    subparser.set_defaults(func=completed)

    subparser = subparsers.add_parser(
        'make_metadata', parents=[output_parser, files_parser, title_parser],
        description=doc_split(make_metadata))
    subparser.set_defaults(func=make_metadata)

    subparser = subparsers.add_parser(
        'transfer', parents=[default_parser, files_parser, title_parser],
        description=doc_split(transfer))
    subparser.set_defaults(func=transfer)

    subparser = subparsers.add_parser(
        'resume', parents=[default_parser],
        description=doc_split(resume))
    subparser.set_defaults(func=resume)

    subparser = subparsers.add_parser(
        'cancel', parents=[default_parser],
        description=doc_split(cancel))
    subparser.set_defaults(func=cancel)

    try:
        args = parser.parse_args()
    except IOError, error:
        parser.error(error)

    try:
        args.func(
            **{k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except (ValueError, IOError, OSError), error:
        parser.error(error)


if __name__ == '__main__':
    main()
