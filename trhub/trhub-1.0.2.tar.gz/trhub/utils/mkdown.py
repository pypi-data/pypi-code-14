import markdown


def html(text):
    return markdown.markdown(text=text, extensions=["markdown.extensions.tables"])


class directionresult:
    def __init__(self):
        self.list = ["|market|code|type|direction|", "|---|---|---|---|"]
        self.up = 0
        self.down = 0
        self.count = 0

    def __add__(self, other):
        self.count += 1
        if float(other[3]) > 0:
            self.up += 1
        elif float(other[3]) < 0:
            self.down += 1
        self.list.append("|".join(other))

    def tomarkdown(self):
        return ["## Total:" + str(self.count), "### UP:" + str(self.up), "### DOWN:" + str(self.down),
                "\r\n".join(self.list)]

    def tohtml(self):
        return html("\r\n".join(self.tomarkdown()))
