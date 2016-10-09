import unicodecsv
from kvtags.models import *


def import_tags_csv(csv_file):
    """Imports tags from a csv file to the database.

    A file instance must be provided as an argument.
    File must be opened beforehand.

    The first row is for tag key.
    The second row is for keys of key-value pairs
    Subsequent rows are values of key-value pairs, one row for each tag instance.

    Example:
    color
    h,s,v,hex
    0,100,50,#7F0000
    30,100,50,#7F3F00
    60,100,50,#7F7F00

    :param csv_file: opened csv file instance
    """
    reader = unicodecsv.reader(csv_file, encoding='utf-8')
    tag_key = reader.next()[0]
    keys = reader.next()

    for row in reader:
        tag = Tag.objects.create(key=tag_key)

        for index, value in enumerate(row):
            tag.add_kv(key=keys[index], value=value)
