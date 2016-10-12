import os
import codecs
import random

class PageManagementUtilities(object):
    def __init__(self):
        pass

    def load_pages(self, page_file_dir, limit=1000000):
        pages = {}
        print page_file_dir
        for subdir, dirs, files in os.walk(page_file_dir):
            for the_file in files:
                if the_file.startswith('.'):
                    continue
                with codecs.open(os.path.join(subdir, the_file), "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')
                pages[the_file] = page_str

        if len(pages.keys()) > limit:
            # if we have too many pages, then we pull out a random sample of pages, of size limit
            page_keys = pages.keys()
            random.shuffle(page_keys)  # randomly order the pages
            #  pull out a subset of pages (0 to limit) from this shuffled set
            final_pages = dict([(fname, pages[fname]) for fname in page_keys[:limit]])
            return final_pages

        return pages

