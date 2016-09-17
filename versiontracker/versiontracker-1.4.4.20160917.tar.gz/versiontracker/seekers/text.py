from versiontracker.baseseekers import BaseSeeker, download


class Seeker(BaseSeeker):

    def __init__(self, data):
        super(Seeker, self).__init__(data)
        self.url = data["url"]
        self.no_date = data.get("no-date", False)

    def data(self):
        text = download(self.url)
        return {
            "id": self.id,
            "version": text,
            "date": None if self.no_date else text,
            "url": self.url,
        }
