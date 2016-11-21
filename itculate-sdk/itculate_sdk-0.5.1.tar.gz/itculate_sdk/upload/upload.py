# noinspection PyPackageRequirements
from unix_dates import UnixDate

from itculate_sdk.data_types.dictionary import Dictionary
from .. import __version__
from ..api import ApiConnection
from ..data_types import Vertex, Edge, TimeSeriesSample


class Upload(object):
    """
    Utility to easily upload data into ITculate.

    This will accumulate the different data reported and send it to the server in the background.
    """
    _vertices = []
    _edges = []
    _samples = []
    _dictionary = []
    _last_update_time = None

    def __init__(self, tenant_id, collector_id, host=None, delay_secs=300, api_key=None, api_secret=None):
        """
        Uploader

        :param str tenant_id: Tenant ID to report for (user must have permissions to access this tenant)
        :param str collector_id: Collector ID (unique within tenant) for this report
        :param str host: Information about the host reporting
        :param int delay_secs: Number of seconds to accumulate reports before uploading
        :param str api_key: (optional) API key to use (will use local_credentials otherwise)
        :param str api_secret:  (optional) API secret to use (will use local_credentials otherwise)
        """
        assert tenant_id and collector_id, "Tenant ID and collector ID are mandatory"

        self._tenant_id = tenant_id
        self._collector_id = collector_id
        self._host = host

        # Create a connection with the 'upload' role
        self._connection = ApiConnection(api_key=api_key, api_secret=api_secret, role="upload")

        # TODO
        self._delay_secs = delay_secs

    @property
    def tenant_id(self):
        return self._tenant_id

    @property
    def collector_id(self):
        return self._collector_id

    @property
    def host(self):
        return self._host

    def upload(self, vertices=None, edges=None, samples=None):
        """
        :param collections.Iterable[Vertex] vertices: Collection of vertices
        :param collections.Iterable[Edge] edges: Collection of edges
        :param collections.Iterable[TimeSeriesSample] samples: Collection of samples
        """
        assert vertices or edges or samples, "No data provided"

        if vertices:
            self._vertices.extend([v.document for v in vertices])

        if edges:
            self._edges.extend([e.document for e in edges])

        if samples:
            self._samples.extend([s.document for s in samples])

        if Dictionary.dictionary_changed:
            self._dictionary = Dictionary.dictionary
            Dictionary.dictionary_changed = False

        # TODO: Move to process on different thread!
        self.flush()

    def flush(self):
        # Get local copies of anything accumulated to far and clean buffers (as atomic as possible)
        l_vertices, l_edges, l_samples, l_dictionary = (self._vertices, self._edges, self._samples, self._dictionary)
        self._vertices, self._edges, self._samples, self._dictionary = ([], [], [], [],)
        self._last_update_time = UnixDate.now()

        if l_vertices or l_edges or l_samples or l_dictionary:
            data = {
                "collector_id": self.collector_id,
                "collector_version": __version__,
                "host": self.host,
                "vertices": l_vertices,
                "edges": l_edges,
                "samples": l_samples,
                "dictionary": l_dictionary,
            }

            self._connection.post("tenants/{}/upload".format(self.tenant_id), json=data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
