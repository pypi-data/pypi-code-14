from ..tecutil import _tecutil, ArgList
from .. import layout
from ..tecutil import lock
from ..exception import TecplotSystemError
from ..tecutil import sv


@lock()
def extract_slice(origin=(0, 0, 0), normal=(0, 0, 1), **kwargs):
    frame, dataset, kwargs = layout.util.kwargs_pop_dataset(**kwargs)

    with frame.activated():
        new_zone_index = dataset.num_zones
        with ArgList() as arglist:
            arglist[sv.ORIGINX] = float(origin[0])
            arglist[sv.ORIGINY] = float(origin[1])
            arglist[sv.ORIGINZ] = float(origin[2])
            arglist[sv.NORMALX] = float(normal[0])
            arglist[sv.NORMALY] = float(normal[1])
            arglist[sv.NORMALZ] = float(normal[2])
            for k, v in kwargs.items():
                arglist[k.upper()] = v
            res = _tecutil.CreateSliceZoneFromPlneX(arglist)
            if not res:
                raise TecplotSystemError()
            return dataset.zone(new_zone_index)
