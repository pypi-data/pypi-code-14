import json
import os
import zipfile

from packaging.version import parse as parse_version

from devpi_server.log import threadlog


def extract_metadata_from_wheel_file(wheel_filename):
    with zipfile.ZipFile(wheel_filename) as zf:
        for meta in zf.namelist():
            if meta.endswith('.dist-info/metadata.json'):
                return json.loads(zf.open(meta).read().decode('utf8'))


def devpiserver_on_upload(stage, project, version, link):
    """ called when a file is uploaded to a private stage for
    a projectname/version.  link.entry.file_exists() may be false because
    a more recent revision deleted the file (and files are not revisioned).
    NOTE that this hook is currently NOT called for the implicit "caching"
    uploads to the pypi mirror.

    If the uploaded file is a wheel and is the latest version on this index,
    store its metadata in json file at the root of index/+f/ directory.
    With the standard config with nginx, nginx will directly serve this file.
    """
    if link.entry and link.entry.file_exists() and link.entry.basename.endswith('.whl'):
        threadlog.info("Wheel detected: %s", link.entry.basename)
        new_version = parse_version(version)
        latest_version = parse_version(stage.get_latest_version_perstage(project))
        if latest_version > new_version:
            threadlog.debug("A newer release has already been uploaded: %s - nothing to do", latest_version)
            return
        metadata = extract_metadata_from_wheel_file(link.entry.file_os_path())
        linkstore = stage.get_linkstore_perstage(link.project, link.version)
        project_dir = '%s/%s/+f/%s' % (linkstore.filestore.storedir, stage.name, project)

        if not os.path.exists(project_dir):
            os.mkdir(project_dir)

        json_path = '%s/%s-%s.json' % (project_dir, project, new_version)
        with open(json_path, 'w') as fd:
            fd.write(json.dumps(metadata))

        threadlog.info("Stored %s to: %s", metadata, json_path)

        # We symlink the latest version
        latest_version_path = '%s/%s.json' % (project_dir, project)
        if os.path.exists(latest_version_path):
            os.unlink(lastest_version_path)
        os.symlink(json_path, latest_version_path)
