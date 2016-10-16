from metraj.compute.pointwise import first_passage_time


def find_static(traj, col_name="static", r=50, min_len=50, varx="attr_VARX", vary="attr_VARY", covxy="attr_COVXY"):
    """
    :param traj:
    :param col_name:
    :param r:
    :param min_len:
    :param varx:
    :param vary:
    :param covxy:
    :return:
    """
    t = traj.copy()
    col_name = "segment_{}".format(col_name)
    t[col_name] = 0

    static_list = []

    itr = t.iterrows()
    ix, first_row = itr.next()

    x0, y0 = first_row[list(t.geo_cols)]
    static_list.append(ix)

    for ix, row in itr:
        x, y = row[list(t.geo_cols)]
        if (x-x0)**2 + (y-y0)**2 < r**2:
            # still in static point
            static_list.append(ix)
            x0, y0 = t.ix[static_list, list(t.geo_cols)].mean().values
        else:
            # out
            if len(static_list) >= min_len:
                keep = static_list[len(static_list) / 2]
                static_list.pop(len(static_list) / 2)
                # mark single point as static
                t.ix[keep, col_name] = 1
                # adjust variance parameters
                t.ix[keep, varx] = r**2
                t.ix[keep, vary] = r**2
                t.ix[keep, covxy] = 0
                # drop all the rest
                t.drop(static_list, axis=0, inplace=True)
            x0, y0 = x, y
            static_list = []

    return t


def find_static_fpt(traj, max_time=30, min_size=20, col_name="static", r=75,
                    varx="attr_VARX", vary="attr_VARY", covxy="attr_COVXY"):
    t = traj.copy()
    col_name = "segment_{}".format(col_name)
    t[col_name] = 0

    t.pointwise_compute(first_passage_time, "FPT")
    is_static = (t.get_comp("FPT") > max_time).values

    groups = []
    grp = []
    for i in range(len(t)):
        if is_static[i]:
            grp.append(traj.index.values[i])
        else:
            if len(grp) >= min_size:
                keep = grp[len(grp) / 2]
                grp.pop(len(grp) / 2)
                # mark a single point as static
                t.ix[keep, [col_name, varx, vary, covxy]] = 1, r**2, r**2, 0
                # delete the rest
                t.drop(grp, axis=0, inplace=True)
            grp = []

    return t

