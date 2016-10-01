#
# growler_sass/middleware.py
#

import sys
import sass
import logging
from pathlib import Path
from os.path import normpath
_log = logging.getLogger(__name__)


class SassMiddleware:
    """
    Middleware class to render SASS files on request.

    The typeinfo variable is the string to be sent as body of the Content-Type header.
        This should probably be left to the default.

    """

    CONTENT_TYPE = 'text/css; charset=UTF-8'
    MATCHING_SUFFIX = '.css'

    def __init__(self, source, dest, **kwargs):
        """
        Construct SASS middleware object, given a source directory and
        the destination URL path on which to host.

        As an example, if the middleware was created with the line:
        `SassMiddleware("/style_sources", '/css')`, and the file '/css/foo.css'
        is detected, the middleware will look for a file '/style_sources'

        Parameters:
            source (str): Name of the directory containing the source
                files. This is resolved by pathlib, so the directory
                must exist and be a directory.

            dest (str): Name of URL prefix which is checked against
                the request path.
            **kwargs: Options which will be forwarded to the sass.compile
                function. Refer to libsass documentation for details.
        """
        self.source_dir = Path(str(source)).resolve()
        if not self.source_dir.is_dir():
            raise NotADirectoryError(source)

        # dest `property` forces starting and endind with forward slash
        self.dest = dest
        self.etag_cache = {}
        self.compile_opts = kwargs

        _log.debug("Serving sass files from {} to {}",
                   self.source_dir,
                   self.dest)

    def matches_request_pattern(self, path):
        """
        If the requested path matches the URL pattern designated by
        this objects's configuration, this function returns the name
        of the equivalent sass file to search for; otherwise it
        returns None.

        The URL pattern means a path starting with the "dest" attribute
        (the directory) and ends with a "MATCHING_SUFFIX" attribute
        file extension.
        """
        if path.startswith(self.dest) and path.endswith(self.MATCHING_SUFFIX):

            start = len(self.dest)

            if isinstance(self.MATCHING_SUFFIX, str):
                stop = -len(self.MATCHING_SUFFIX)
            else:
                for suffix in self.MATCHING_SUFFIX:
                    if path.endswith(suffix):
                        stop = -len(suffix)
                        break

            filename = path[start:stop] + '.sass'
            return filename

    def get_etag(self, filepath):
       """
       Return the etag of the hh
       """
       file_info = filepath.stat()
       mod_time = file_info.st_mtime
       inode = file_info.st_ino
       size = file_info.st_size
       etag = '%x-%x' % (size, int(mod_time + inode))
       return etag

    def __call__(self, req, res):
        """
        Called with a req, res pair. If the request path matches the
        dest dir, and a SASS file exists with the same name (with
        .sass suffix), the file is compiled and the result is sent
        to the response.
        """
        # security feature - do not allow "path escalation" via ..
        if '..' in req.path:
            return None

        matching_filename = self.matches_request_pattern(normpath(req.path))

        if not matching_filename:
            return

        _log.debug("Potential requested path {}", req.path)

        sass_file = self.source_dir / matching_filename

        if sass_file.is_file():
            _log.debug("Found matching SASS file: {}", sass_file)

            etag = self.get_etag(sass_file)

            res.headers['Etag'] = etag
            requested_etag = req.headers.get('IF-NONE-MATCH', None)

            if requested_etag == etag:
                res.status_code = 304
                res.end()
                return

            try:
                result = self.etag_cache[etag]
            except:
                result = sass.compile(filename=str(sass_file),
                                      **self.compile_opts)
                self.etag_cache[etag] = result
            res.headers['Content-Type'] = self.CONTENT_TYPE
            res.send(result.encode())

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, path):
        self._dest = '/%s/' % path.strip('/')
