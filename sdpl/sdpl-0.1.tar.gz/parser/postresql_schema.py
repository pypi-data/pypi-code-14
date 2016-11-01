__author__ = 'Bohdan Mushkevych'

from schema.sdpl_schema import Schema, Field, MIN_VERSION_NUMBER, VARCHAR_DEFAULT_LENGTH, DataType
from parser.data_sink import DataSink
from parser.data_source import DataSource


PGSQL_MAPPING = {
    DataType.INTEGER.name: 'INTEGER',
    DataType.LONG.name: 'BIGINT',
    DataType.FLOAT.name: 'DOUBLE PRECISION',
    DataType.CHARARRAY.name: 'VARCHAR',
    DataType.BYTEARRAY.name: 'BYTEA',
    DataType.BOOLEAN.name: 'BOOLEAN',
    DataType.DATETIME.name: 'TIMESTAMP',
}


def parse_field(field:Field):
    pgsql_type = PGSQL_MAPPING[field.data_type]
    if field.data_type == 'CHARARRAY':
        length = field.max_length if field.max_length else VARCHAR_DEFAULT_LENGTH
        pgsql_type += '({0})'.format(length)

    out = '{0}\t{1}'.format(field.name, pgsql_type)
    if field.is_nullable:
        out += '\t{0}'.format('NOT NULL')
    if field.is_unique:
        out += '\t{0}'.format('UNIQUE')
    if field.is_primary_key:
        out += '\t{0}'.format('PRIMARY KEY')
    if field.default:
        out += '\t{0}\t{1}'.format('DEFAULT', field.default)

    return out


def parse_schema(schema:Schema, max_version=MIN_VERSION_NUMBER):
    filtered_fields = [f for f in schema.fields if f.version <= max_version]
    out = ',\n    '.join([parse_field(field) for field in filtered_fields])
    out = '\n    ' + out + '\n'
    return out


def parse_datasink(data_sink:DataSink):
    raise NotImplementedError('postgresql_schema.parse_datasink not yet implemented')


def parse_datasource(data_source:DataSource):
    raise NotImplementedError('postgresql_schema.data_source not yet implemented')
