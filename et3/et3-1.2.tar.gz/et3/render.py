from .utils import is_seq
from collections import OrderedDict

EXCLUDE_ME = 0xDEADC0DE

def doall(v, pipeline):
    for x in pipeline:
        v = x(v) if callable(x) else x
    return v

def render_item(description, item):
    result = OrderedDict() if isinstance(description, OrderedDict) else {}
    for key, pipeline in description.items():
        if isinstance(pipeline, dict):
            sub_description = pipeline
            rendered = render_item(sub_description, item)
        elif isinstance(pipeline, list):
            rendered = doall(item, pipeline)
        elif callable(pipeline):
            rendered = pipeline(doall, item)
        else:
            raise AssertionError("render pipeline for item is an unhandled type: %r" % type(pipeline))
        if rendered == EXCLUDE_ME:
            # pipeline has indicated this key should be discarded from the results
            continue
        result[key] = rendered
    return result

def render(description, data):
    assert is_seq(data), "data must be a sequence of values, not %r" % type(data)
    return map(lambda item: render_item(description, item), data)
