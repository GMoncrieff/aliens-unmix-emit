
import argparse
import numpy as np
import pandas as pd
import xarray as xr
from emit_tools import emit_xarray

#root_dir = '/home/glenn/emit/'
#refl_file = 'data/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc'
#point_file = 'data/sample_coords_long.csv'

def extract(root_dir, refl_file, point_file):
    #path to emit refl data
    fp = root_dir + refl_file

    #read data
    ds = emit_xarray(fp)
    ds

    #path to points for spectral lib
    #should be comma delim with cols ID (int) ,Category (str),Latitude (dbl),Longitude (dbl)
    #in EPSG 4326 projection
    points = pd.read_csv(root_dir + point_file)

    #extract reflectance at points
    points = points.set_index(['ID'])
    xp = points.to_xarray()
    extracted = ds.sel(latitude=xp.Latitude,longitude=xp.Longitude, method='nearest').to_dataframe()
    df = extracted.join(points['Category'], on=['ID'])
    df_long = df[['Category','reflectance','wavelengths']].reset_index()
    df.loc[:]['reflectance'][df.loc[:]['reflectance'] == -0.01] = 0
    df_long = df[['Category','reflectance','wavelengths']].reset_index()
    df_cat = df_long[['ID', 'Category']].drop_duplicates(subset='ID')

    #convert long to wide df with a column for each wavelength. add column for the category of each point
    df_wide = df_long.pivot(index='ID', columns='wavelengths', values='reflectance')
    df_final = df_cat.set_index('ID').join(df_wide)
    #drop index from df
    df_final.reset_index(inplace=True)
    #drop category column
    df_final.drop(columns=['ID'], inplace=True)
    #fill na
    df_final.fillna(0, inplace=True)
    #write spectral library to csv
    df_final.to_csv(root_dir + 'data/example_lib.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='extract spectral library')
    parser.add_argument('root_dir', type=str, help='Root directory for processing')
    parser.add_argument('refl_file', type=str, help='EMIT reflectance netcdf')
    parser.add_argument('point_file', type=str, help='sample points')

    args = parser.parse_args()
    extract(args.root_dir, args.refl_file, args.point_file)
