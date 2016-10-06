import re


class Canonicalization:
    @staticmethod
    def canonicalize(text):
        return re.sub('\W+', '', str(text)).lower()
