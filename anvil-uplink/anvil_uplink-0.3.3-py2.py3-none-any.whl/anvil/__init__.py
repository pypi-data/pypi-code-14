import sys

__author__ = 'Meredydd Luff <meredydd@anvil.works>'


class LiveObject():
    def __init__(self, spec):
        self._spec = spec

    def __repr__(self):
        return "<LiveObject: " + self._spec["backend"] + ">"

    def __eq__(self, other):
      return isinstance(other, LiveObject) and other._spec["id"] == self._spec["id"] and other._spec["backend"] == self._spec["backend"]

    def __ne__(self, other):
      return not self.__eq__(other)



class Media:
    def __getattr__(self, item):
        if item == "url":
            return self.get_url()
        elif item == "content_type":
            return self.get_content_type()
        elif item == "name":
            return self.get_name()
        elif item == "length":
            return self.get_length()
        else:
            raise AttributeError

    def get_url(self, download=True):
        return None

    def get_bytes(self):
        raise Exception("get_bytes() not implemented")

    def get_length(self):
        return len(self.get_bytes())

    def get_name(self):
        return None


class BlobMedia(Media):
    def __init__(self, content_type, content, name=None):
        self._content_type = content_type
        if sys.version_info >= (3,) and isinstance(content, str):
          content = content.encode()
        self._bytes = content
        self._name = name

    def get_content_type(self):
        return self._content_type

    def get_bytes(self):
        return self._bytes

    def get_name(self):
        return self._name

    def __repr__(self):
        return "BlobMedia[%s,%d bytes%s]" % (self._content_type, len(self._bytes), (",name=" + self._name if self._name is not None else ""))

DataMedia = BlobMedia


class URLMedia(Media):
    def __init__(self, url):
        self._url = url
        self._content_type = None

    def get_url(self, download=True):
        return self._url

    def get_bytes(self):
        import anvil.server

        return anvil.server.call("anvil.private.http.request", url=url).get_bytes()

    def get_content_type(self):
        if self._content_type is None:
            import anvil.server

            self._content_type = anvil.server.call("anvil.private.http.request", url=url).content_type

        return self._content_type


def is_server_side():
    return True
