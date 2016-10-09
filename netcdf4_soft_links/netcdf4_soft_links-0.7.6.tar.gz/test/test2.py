import h5py
file_name='/data/home/laliberte/CDB/2.0/sea_ice_landfast/obs/ORA/out_CA_obs/Mercator/GLORYS2V3/reanalysis/day/seaIce/day/r1i1p1/v20160728/sic/sic_day_GLORYS2V3_reanalysis_199401-201412.nc'
test=h5py.File(file_name)
getitem_tuple=(slice(1023, 1075, 1), slice(0, 144, 1), slice(0, 223, 1))
data=test['sic'][getitem_tuple]
print(data.shape)
