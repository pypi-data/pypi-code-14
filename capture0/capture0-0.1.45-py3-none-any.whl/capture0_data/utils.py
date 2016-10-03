from urllib.request import urlopen


def csv_lines(url):
    with urlopen(url) as f:
        for line in f:
            yield line.decode("utf-8")
