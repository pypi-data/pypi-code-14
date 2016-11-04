from floraconcierge.client.types import Object


class Count(Object):
    """
    :type id: int
    """

    def __init__(self, *args, **kwargs):
        self.count = None
        self.id = None
        self.inflect1 = None
        self.inflect2 = None
        self.inflect3 = None
        self.inflect4 = None
        self.inflect5 = None
        self.inflect6 = None
        self.word = None

        super(Count, self).__init__(*args, **kwargs)
