class Client:
    def get(self, url, data=None):
        """
        Opens url using GET.

        Return a Page() instance.
        """

        raise NotImplementedError

    def post(self, url, data=None):
        """
        Opens url using POST.

        Return a Page() instance.
        """

        raise NotImplementedError