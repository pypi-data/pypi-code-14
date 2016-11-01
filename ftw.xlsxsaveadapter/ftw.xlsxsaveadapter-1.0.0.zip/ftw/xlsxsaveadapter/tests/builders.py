from ftw.builder import builder_registry
from ftw.builder.archetypes import ArchetypesBuilder


class FormFolderBuilder(ArchetypesBuilder):
    portal_type = 'FormFolder'

builder_registry.register('form folder', FormFolderBuilder)


class XlsxAdapterBuilder(ArchetypesBuilder):
    portal_type = 'XlsxDataAdapter'

builder_registry.register('xlsx data adapter', XlsxAdapterBuilder)
