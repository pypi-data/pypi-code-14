from invisibleroads_macros.disk import (
    get_file_extension, make_folder, resolve_relative_path)
from invisibleroads_macros.security import make_random_string
from invisibleroads_posts.views import expect_param
from os import rename
from os.path import basename, join
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from shutil import copyfileobj
from tempfile import mkdtemp

from .models import Upload


def add_routes(config):
    config.add_route('files.json', '/files.json')

    config.add_view(
        receive_file,
        permission='upload-file',
        renderer='json',
        request_method='POST',
        route_name='files.json')


def receive_file(request):
    try:
        field_storage = request.POST['files[]']
    except KeyError:
        raise HTTPBadRequest
    source_file = field_storage.file
    source_name = basename(field_storage.filename)
    source_extension = get_file_extension(source_name)

    settings = request.registry.settings
    data_folder = settings['data.folder']
    user_id = request.authenticated_userid or 0
    target_folder = make_upload_folder(
        data_folder, user_id, settings['uploads.tokens.length'])
    target_path = join(target_folder, 'raw' + source_extension)

    temporary_path = join(target_folder, 'temporary.bin')
    with open(temporary_path, 'wb') as temporary_file:
        copyfileobj(source_file, temporary_file)
    rename(temporary_path, target_path)

    open(join(target_folder, 'name.txt'), 'wt').write(source_name)
    return {
        'upload_id': basename(target_folder),
    }


def get_upload_from(request):
    upload_id = expect_param('upload_id', request.params)
    try:
        upload = get_upload(request, upload_id)
    except IOError:
        raise HTTPNotFound({'upload_id': 'bad'})
    return upload


def make_upload_folder(data_folder, user_id, token_length):
    user_id = str(user_id or 0)
    user_upload_folder = make_folder(join(data_folder, 'uploads', user_id))
    return mkdtemp(
        suffix=make_random_string(token_length - 6),
        prefix='', dir=user_upload_folder)


def get_upload(request, upload_id):
    settings = request.registry.settings
    data_folder = settings['data.folder']
    user_id = request.authenticated_userid or 0
    parent_folder = join(data_folder, 'uploads')
    source_folder = resolve_relative_path(join(
        str(user_id), upload_id), parent_folder)
    return Upload(source_folder)
