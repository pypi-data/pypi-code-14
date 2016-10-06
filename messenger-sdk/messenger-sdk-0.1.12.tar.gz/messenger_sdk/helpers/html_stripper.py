from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

    @staticmethod
    def _strip_tags(html):
        s = HTMLStripper()
        s.feed(html)
        return s.get_data()

    @staticmethod
    def strip(data):
        if isinstance(data, str):
            return HTMLStripper._strip_tags(data)
        elif isinstance(data, dict):
            for key, value in data.items():
                value = HTMLStripper.strip(value)
                data.update({
                    key: value
                })
        elif isinstance(data, list):
            for item in data:
                HTMLStripper.strip(item)

        return data
