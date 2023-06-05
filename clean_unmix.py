import argparse
import rioxarray as riox
import geopandas as gpd
import xarray as xr
import numpy as np

#root_dir = '/home/glenn/emit/'
#ncfile = 'data/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc'
#mesmafile = 'SpectralUnmixing/mesma_test_fractional_cover'

def process(root_dir, ncfile, mesmafile, mask):
    print('writing geographic data')

    #file paths
    #1 the raw emit netcdf reflectance
    fpnc = root_dir + ncfile
    #2 the output from mesma in envi format
    fpmesma = root_dir +  mesmafile
        
    #open location data
    loc = xr.open_dataset(fpnc, engine = 'h5netcdf', group='location')
    #open actual data
    ds = xr.open_dataset(fpnc, engine = 'h5netcdf')
    #open unmixing results
    mes = riox.open_rasterio(fpmesma)
    #get location metadata
    GT = ds.geotransform
    sref = ds.spatial_ref

    #create loc array
    GLT_NODATA_VALUE=0
    glt_array = np.nan_to_num(np.stack([loc['glt_x'].data,loc['glt_y'].data],axis=-1),nan=GLT_NODATA_VALUE).astype(int)

    #actual data
    ds_array = mes.data
    ds_array =np.transpose(ds_array, (1, 2, 0))

    # Build Output Dataset
    fill_value = -9999
    out_ds = np.zeros((glt_array.shape[0], glt_array.shape[1], ds_array.shape[-1]), dtype=np.float32) + fill_value
    valid_glt = np.all(glt_array != GLT_NODATA_VALUE, axis=-1)

    # Adjust for One based Index
    glt_array[valid_glt] -= 1 
    # Use indexing/broadcasting to populate array cells with 0 values
    out_ds[valid_glt, :] = ds_array[glt_array[valid_glt, 1], glt_array[valid_glt, 0], :]

    # Create Array for Lat and Lon and fill
    dim_x = loc.glt_x.shape[1]
    dim_y = loc.glt_x.shape[0]
    lon = np.zeros(dim_x)
    lat = np.zeros(dim_y)
    #Calclutate the latitude and longitude for each row (x_dim) and column (y_dim) of the dataset.
    for x in np.arange(dim_x):
        x_geo = GT[0] + x * GT[1]
        lon[x] = x_geo
    for y in np.arange(dim_y):
        y_geo = GT[3] + y * GT[5]
        lat[y] = y_geo

    #create xarray
    coords = {'y':(['y'],lat), 'x':(['x'],lon),'bands':(['bands'],mes.band.data)} ## ** upacks the existing dictionary from the wvl dataset.
    data_vars = {'band':(['y','x','bands'], out_ds)}
    out_xr = xr.Dataset(data_vars=data_vars, coords=coords, attrs=mes.attrs)
    out_xr.coords['y'].attrs = loc['lat'].attrs
    out_xr.coords['x'].attrs = loc['lon'].attrs
    # Add CRS in easily recognizable format
    out_xr.rio.write_crs(sref,inplace=True)
    #repalce na
    out_xr['band'].data[out_xr['band'].data == fill_value] = np.nan

    print('masking to natural vegetation')

    #masking
    if mask:
        #intact natural vegetaition 
        rle = gpd.read_file(root_dir + 'data/NBA2018_Terr_RLE_PL_remnants.shp')
        #reproject ext to match rle crs
        rle= rle.to_crs('EPSG:4326')
        #keep on the rows that intersect with the ext
        xmin, ymin, xmax, ymax = out_xr.rio.bounds()
        rle = rle.cx[xmin:xmax, ymin:ymax]
        #clip
        out_xr_clip = out_xr.rio.clip(rle.geometry.values,all_touched=True)
        #write raster
        print('writing raster')
        out_xr_clip.band.transpose('bands', 'y', 'x').rio.to_raster("data/aliens_cog.tif",driver='COG')
    else:
        print('writing raster')
        out_xr_clip.band.transpose('bands', 'y', 'x').rio.to_raster("data/aliens_cog.tif",driver='COG')
    
    print('done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='clean spectral unmixing results.')
    parser.add_argument('--root_dir', type=str, help='Root directory for processing')
    parser.add_argument('--ncfile', type=str, help='EMIT reflectance netcdf')
    parser.add_argument('--mesmafile', type=str, help='EMIT unmixing result')
    parser.add_argument('--mask', type=bool, default=False, help='Mask to natural vegetation')
    args = parser.parse_args()
    process(args.root_dir, args.ncfile, args.mesmafile, args.mask)
