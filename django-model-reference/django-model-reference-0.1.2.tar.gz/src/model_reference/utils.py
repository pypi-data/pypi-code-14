def normalize_name(name, model=None):
    """
    Return the expanded name from name and model class. If model is given,
    treats name as a suffix.
    """

    if model is None:
        return name
    else:
        meta = model._meta
        return '%s.%s:%s' % (meta.app_label, meta.model_name, name)
