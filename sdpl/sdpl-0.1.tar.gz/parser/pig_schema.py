__author__ = 'Bohdan Mushkevych'

from schema.sdpl_schema import Schema, Field, MIN_VERSION_NUMBER
from parser.data_sink import DataSink
from parser.data_source import DataSource


def parse_field(field:Field):
    out = '{0}:{1}'.format(field.name, field.data_type)
    return out


def parse_schema(schema:Schema, max_version=MIN_VERSION_NUMBER):
    filtered_fields = [f for f in schema.fields if f.version <= max_version]
    out = ',\n    '.join([parse_field(field) for field in filtered_fields])
    out = '\n    ' + out + '\n'
    return out


def parse_datasink(data_sink:DataSink):
    # TODO: add specifics via USING PigStorage/BinStorage/JsonStorage
    load_string = "STORE INTO '{0}:{1}/{2}/{3}' USING PigStorage(',') ;".format(
        data_sink.data_repository.host,
        data_sink.data_repository.port,
        data_sink.data_repository.db,
        data_sink.table_name)
    return load_string


def parse_datasource(data_source:DataSource):
    # TODO: add specifics via USING PigStorage/BinStorage/JsonStorage
    load_string = "LOAD '{0}:{1}/{2}/{3}' USING PigStorage(',') AS ({4})".format(
        data_source.data_repository.host,
        data_source.data_repository.port,
        data_source.data_repository.db,
        data_source.table_name,
        parse_schema(data_source.relation.schema))
    return load_string
