# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vector_tile.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='vector_tile.proto',
  package='mapnik.vector',
  syntax='proto2',
  serialized_pb=b'\n\x11vector_tile.proto\x12\rmapnik.vector\"\xc5\x04\n\x04tile\x12)\n\x06layers\x18\x03 \x03(\x0b\x32\x19.mapnik.vector.tile.layer\x1a\xa1\x01\n\x05value\x12\x14\n\x0cstring_value\x18\x01 \x01(\t\x12\x13\n\x0b\x66loat_value\x18\x02 \x01(\x02\x12\x14\n\x0c\x64ouble_value\x18\x03 \x01(\x01\x12\x11\n\tint_value\x18\x04 \x01(\x03\x12\x12\n\nuint_value\x18\x05 \x01(\x04\x12\x12\n\nsint_value\x18\x06 \x01(\x12\x12\x12\n\nbool_value\x18\x07 \x01(\x08*\x08\x08\x08\x10\x80\x80\x80\x80\x02\x1ar\n\x07\x66\x65\x61ture\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x10\n\x04tags\x18\x02 \x03(\rB\x02\x10\x01\x12\x33\n\x04type\x18\x03 \x01(\x0e\x32\x1c.mapnik.vector.tile.GeomType:\x07Unknown\x12\x14\n\x08geometry\x18\x04 \x03(\rB\x02\x10\x01\x1a\xb1\x01\n\x05layer\x12\x12\n\x07version\x18\x0f \x02(\r:\x01\x31\x12\x0c\n\x04name\x18\x01 \x02(\t\x12-\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x1b.mapnik.vector.tile.feature\x12\x0c\n\x04keys\x18\x03 \x03(\t\x12)\n\x06values\x18\x04 \x03(\x0b\x32\x19.mapnik.vector.tile.value\x12\x14\n\x06\x65xtent\x18\x05 \x01(\r:\x04\x34\x30\x39\x36*\x08\x08\x10\x10\x80\x80\x80\x80\x02\"?\n\x08GeomType\x12\x0b\n\x07Unknown\x10\x00\x12\t\n\x05Point\x10\x01\x12\x0e\n\nLineString\x10\x02\x12\x0b\n\x07Polygon\x10\x03*\x05\x08\x10\x10\x80@B\x02H\x03'
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_TILE_GEOMTYPE = _descriptor.EnumDescriptor(
  name='GeomType',
  full_name='mapnik.vector.tile.GeomType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Unknown', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Point', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LineString', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Polygon', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=548,
  serialized_end=611,
)
_sym_db.RegisterEnumDescriptor(_TILE_GEOMTYPE)


_TILE_VALUE = _descriptor.Descriptor(
  name='value',
  full_name='mapnik.vector.tile.value',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_value', full_name='mapnik.vector.tile.value.string_value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='float_value', full_name='mapnik.vector.tile.value.float_value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='mapnik.vector.tile.value.double_value', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='mapnik.vector.tile.value.int_value', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uint_value', full_name='mapnik.vector.tile.value.uint_value', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sint_value', full_name='mapnik.vector.tile.value.sint_value', index=5,
      number=6, type=18, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='mapnik.vector.tile.value.bool_value', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(8, 536870912), ],
  oneofs=[
  ],
  serialized_start=89,
  serialized_end=250,
)

_TILE_FEATURE = _descriptor.Descriptor(
  name='feature',
  full_name='mapnik.vector.tile.feature',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='mapnik.vector.tile.feature.id', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tags', full_name='mapnik.vector.tile.feature.tags', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), b'\020\001')),
    _descriptor.FieldDescriptor(
      name='type', full_name='mapnik.vector.tile.feature.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='geometry', full_name='mapnik.vector.tile.feature.geometry', index=3,
      number=4, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), b'\020\001')),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=252,
  serialized_end=366,
)

_TILE_LAYER = _descriptor.Descriptor(
  name='layer',
  full_name='mapnik.vector.tile.layer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='mapnik.vector.tile.layer.version', index=0,
      number=15, type=13, cpp_type=3, label=2,
      has_default_value=True, default_value=1,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='mapnik.vector.tile.layer.name', index=1,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='features', full_name='mapnik.vector.tile.layer.features', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='keys', full_name='mapnik.vector.tile.layer.keys', index=3,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='values', full_name='mapnik.vector.tile.layer.values', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='extent', full_name='mapnik.vector.tile.layer.extent', index=5,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=4096,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(16, 536870912), ],
  oneofs=[
  ],
  serialized_start=369,
  serialized_end=546,
)

_TILE = _descriptor.Descriptor(
  name='tile',
  full_name='mapnik.vector.tile',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='layers', full_name='mapnik.vector.tile.layers', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_TILE_VALUE, _TILE_FEATURE, _TILE_LAYER, ],
  enum_types=[
    _TILE_GEOMTYPE,
  ],
  options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(16, 8192), ],
  oneofs=[
  ],
  serialized_start=37,
  serialized_end=618,
)

_TILE_VALUE.containing_type = _TILE
_TILE_FEATURE.fields_by_name['type'].enum_type = _TILE_GEOMTYPE
_TILE_FEATURE.containing_type = _TILE
_TILE_LAYER.fields_by_name['features'].message_type = _TILE_FEATURE
_TILE_LAYER.fields_by_name['values'].message_type = _TILE_VALUE
_TILE_LAYER.containing_type = _TILE
_TILE.fields_by_name['layers'].message_type = _TILE_LAYER
_TILE_GEOMTYPE.containing_type = _TILE
DESCRIPTOR.message_types_by_name['tile'] = _TILE

tile = _reflection.GeneratedProtocolMessageType('tile', (_message.Message,), dict(

  value = _reflection.GeneratedProtocolMessageType('value', (_message.Message,), dict(
    DESCRIPTOR = _TILE_VALUE,
    __module__ = 'vector_tile_pb2_p3'
    # @@protoc_insertion_point(class_scope:mapnik.vector.tile.value)
    ))
  ,

  feature = _reflection.GeneratedProtocolMessageType('feature', (_message.Message,), dict(
    DESCRIPTOR = _TILE_FEATURE,
    __module__ = 'vector_tile_pb2_p3'
    # @@protoc_insertion_point(class_scope:mapnik.vector.tile.feature)
    ))
  ,

  layer = _reflection.GeneratedProtocolMessageType('layer', (_message.Message,), dict(
    DESCRIPTOR = _TILE_LAYER,
    __module__ = 'vector_tile_pb2_p3'
    # @@protoc_insertion_point(class_scope:mapnik.vector.tile.layer)
    ))
  ,
  DESCRIPTOR = _TILE,
  __module__ = 'vector_tile_pb2_p3'
  # @@protoc_insertion_point(class_scope:mapnik.vector.tile)
  ))
_sym_db.RegisterMessage(tile)
_sym_db.RegisterMessage(tile.value)
_sym_db.RegisterMessage(tile.feature)
_sym_db.RegisterMessage(tile.layer)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), b'H\003')
_TILE_FEATURE.fields_by_name['tags'].has_options = True
_TILE_FEATURE.fields_by_name['tags']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), b'\020\001')
_TILE_FEATURE.fields_by_name['geometry'].has_options = True
_TILE_FEATURE.fields_by_name['geometry']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), b'\020\001')
# @@protoc_insertion_point(module_scope)
