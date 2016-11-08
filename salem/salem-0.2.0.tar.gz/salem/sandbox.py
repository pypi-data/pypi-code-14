import salem
from salem import get_demo_file, sio
from numpy.testing import assert_allclose
import numpy as np
import time

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle
from matplotlib.path import Path
from matplotlib.ticker import NullLocator, Formatter, FixedLocator
from matplotlib.transforms import Affine2D, BboxTransformTo, Transform, IdentityTransform
from matplotlib.projections import register_projection
import matplotlib.spines as mspines
import matplotlib.axis as maxis


class SalemTransform(Transform):
    """
    The base Hammer transform.
    """

    input_dims = 2
    output_dims = 2
    is_separable = False
    has_inverse = False

    def __init__(self, target_grid=None, source_grid=None):

        self.source_grid = source_grid
        self.target_grid = target_grid
        Transform.__init__(self)

    def transform_non_affine(self, xy):
        """
        Override the transform_non_affine method to implement the custom
        transform.

        The input and output are Nx2 numpy arrays.
        """
        xx = xy[:, 0:1]
        yy = xy[:, 1:2]
        if self.source_grid is not None:
            xx, yy = self.target_grid.transform(xx, yy, crs=self.source_grid.proj)

        return np.concatenate((xx, yy), 1)


# get the data at the latest time step
ds = salem.open_wrf_dataset(salem.get_demo_file('wrfout_d01.nc')).isel(time=-1)

# get the wind data at 10000 m a.s.l.
u = ds.salem.wrf_zlevel('U', 10000.)
v = ds.salem.wrf_zlevel('V', 10000.)
# ws = ds.salem.wrf_zlevel('WS', 10000.)
# u = ds.U.isel(bottom_top=12)
# v = ds.V.isel(bottom_top=12)
# ws = ds.WS.isel(bottom_top=12)

# get the axes ready
f, ax = plt.subplots()

# plot the salem map background, make countries in grey
smap = ds.salem.get_map(countries=False)
smap.set_shapefile(countries=True, color='grey')
smap.plot(ax=ax)


# Quiver only every 7th grid point
u = u[4::7, 4::7]
v = v[4::7, 4::7]

# transform their coordinates to the map reference system and plot the arrows
xx, yy = smap.grid.transform(u.west_east.values, u.south_north.values,
                             crs=ds.salem.grid.proj)
xx, yy = u.west_east.values, u.south_north.values
xx, yy = np.meshgrid(xx, yy)
qu = ax.quiver(xx, yy, u.values, v.values, transform=SalemTransform(smap.grid, ds.salem.grid))

plt.show()


# start_time = time.time()
# ws_h = ds.isel(time=1).salem.wrf_zlevel('WS', levels=8000.,
#                                         use_multiprocessing=False)
# print("--- %s seconds ---" % (time.time() - start_time))
#
# assert np.all(np.isfinite(ws_h))
#
# start_time = time.time()
# ws_h2 = ds.isel(time=1).salem.wrf_zlevel('WS', levels=8000.)
# print("--- %s seconds ---" % (time.time() - start_time))
#
# assert_allclose(ws_h, ws_h2, atol=1e-5)