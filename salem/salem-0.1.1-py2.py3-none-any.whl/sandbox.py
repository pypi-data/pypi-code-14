import numpy as np
import xarray as xr
import salem

# da = xr.DataArray(np.arange(20).reshape(4, 5), dims=['lat', 'lon'],
#                   coords={'lat':np.linspace(0, 30, 4), 'lon':np.linspace(-20, 20, 5)})
#
# # da.salem.quick_map()
#
# fpath = salem.get_demo_file('himalaya.tif')
# ds = salem.open_xr_dataset(fpath)
#
# hmap = ds.salem.get_map(cmap='topo')
# hmap.set_data(ds['data'])
# hmap.visualize()

dutm = xr.DataArray(np.arange(20).reshape(4, 5), dims=['y', 'x'],
                    coords={'y': np.arange(3, 7)*2e5,
                            'x': np.arange(3, 8)*2e5})
dutm.attrs['pyproj_srs'] = 'epsg:32630'  # http://spatialreference.org/ref/epsg/wgs-84-utm-zone-30n/

dutm.salem.quick_map()
import matplotlib.pyplot as plt
plt.show()