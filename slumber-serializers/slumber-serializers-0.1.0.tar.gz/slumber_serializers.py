import unicodecsv as csv
from six import BytesIO
from slumber import serialize


class CsvSerializer(serialize.BaseSerializer):
    key = 'csv'
    content_types = ['text/csv']

    def loads(self, data):
        output = BytesIO(data)
        return csv.reader(output)

    def dumps(self, data):
        output = BytesIO()
        csv.writer(output).writerows(data)
        return output.getvalue()


class BinarySerializer(serialize.BaseSerializer):
    key = 'binary'
    content_types = ['image/gif']

    def loads(self, data):
        output = BytesIO(data)
        return output.getvalue()

    def dumps(self, data):
        output = BytesIO(data)
        return output.getvalue()
