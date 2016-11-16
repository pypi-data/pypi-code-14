
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^juta_cms_icons\.fields\.IconField"])
except ImportError:
    pass