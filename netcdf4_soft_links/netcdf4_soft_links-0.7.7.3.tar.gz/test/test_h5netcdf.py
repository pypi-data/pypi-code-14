import h5netcdf.legacyapi as netCDF4_h5
#import netCDF4

#file_name='orog_fx_MRI-CGCM3_amip_r0i0p0.nc'
file_name='test.nc'
#dataset=netCDF4.Dataset(file_name,'r')
dataset=netCDF4_h5.Dataset(file_name,'r')
groups =dataset.groups.keys()
print(groups)

dataset.close()

quit()
