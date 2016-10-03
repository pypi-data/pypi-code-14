import re

from collections import UserString


class Loom(UserString):

    def __init__(self, data, **kwargs):
        super().__init__(str)
        self.data = data
        self.language = None

        if 'language' not in kwargs:
            self.language = 'english'
        else:
            self.language = kwargs['language']

    def stringify(self):
        return str(self.data)

    def rm_lines(self):
        return self.__class__(
            self.data
                .replace('-\n ', '').replace('- \n', '').replace('-\n', '')
                .replace(' - ', '').replace('- ', '').replace(' -', '')
                .replace('\n', ' ')
        )

    def rm_num(self):
        return self.__class__(re.sub("\d+", "", self.data))

    def rm_nonchar(self):
        if self.language == 'greek':
            clean_text = "".join(re.findall("([ʹ-Ϋά-ϡἀ-ᾯᾰ-῾ ])", self.data))
        else:
            clean_text = "".join(re.findall("([A-Za-z ])"), self.data)
        return self.__class__(clean_text)

    def rm_edits(self):
        return self.__class__(
            re.sub("\〚(.*?)\〛", "", re.sub("\{(.*?)\}", "", re.sub(
                "\((.*?)\)", "", re.sub("\<(.*?)\>", "", re.sub(
                    "\[(.*?)\]", "", self.data)))))
        )

    def rm_spaces(self):
        rexr = re.compile(r'\W+')
        clean_text = rexr.sub(' ', self.data)
        return self.__class__(clean_text.strip())

    def scrub(self):
        return (
            self.rm_lines().rm_edits()
            .rm_nonchar(self.language).rm_spaces().stringify()
        )
