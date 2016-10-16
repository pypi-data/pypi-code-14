
from metraj.smoothing.simple import FilterByCol


def idin(l):
    return lambda t: t.id in l


def filter_compute(ts, pointwise_function, col_name, decision_function, filtered_name):
    ts.pointwise_compute(pointwise_function, col_name)
    filt_ = FilterByCol("comp_{}".format(col_name), decision_function)
    ts.trajectory_compute(filt_.filter, filtered_name)
    return ts


def filter_under(ts, pointwise_function, name, under):
    return filter_compute(ts, pointwise_function,
                          col_name=name,
                          decision_function=lambda val: val<under,
                          filtered_name="{} < {}".format(name, under))


def filter_static(ts, static_finder, name="static-parts", static_col = "segment_static"):
    ts.trajectory_compute(static_finder, "temp-static")
    ts.combine(ts, ts.depth-1, ts.depth, combine_f=lambda ts_1, ts_2: ts_2[static_col], name=name)
    return ts