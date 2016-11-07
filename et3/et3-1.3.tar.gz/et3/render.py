from .utils import is_seq
from collections import OrderedDict

EXCLUDE_ME = 0xDEADC0DE

def do(item, segment):
    return segment(item) if callable(segment) else segment

def doall(item, pipeline):
    for seg in pipeline:
        if callable(seg):
            item = seg(item)
        elif isinstance(seg, tuple):
            item = tuple([do(item, subseg) for subseg in seg])
        else:
            item = seg
    return item

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
