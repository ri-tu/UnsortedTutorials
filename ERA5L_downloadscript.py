import xarray as xr
import matplotlib.pyplot as plt
import geopandas as gpd
import rioxarray
import cdsapi
import os

print("successfully imported")
## Set the user defined parameters

# Path to the ROI shapefile
shp=gpd.read_file('Bounds/north_sikkim_bound.shp')
gpd_bounds=shp.total_bounds
aoi=[gpd_bounds[3],gpd_bounds[0],gpd_bounds[1],gpd_bounds[2],]

print("successfully generated shapefile bounds")
# Name of dataset as given on CDS
dat_name='reanalysis-era5-land-monthly-means'

# Format is netcdf or grib
format='netcdf'

# List of variables as given in CDS
var_list=['total_precipitation']

# Year, month,day and times required
year=['1950', '1951', '1952',
            '1953', '1954', '1955',
            '1956', '1957', '1958',
            '1959', '1960', '1961',
            '1962', '1963', '1964',
            '1965', '1966', '1967',
            '1968', '1969', '1970',
            '1971', '1972', '1973',
            '1974', '1975', '1976',
            '1977', '1978', '1979',
            '1980', '1981', '1982',
            '1983', '1984', '1985',
            '1986', '1987', '1988',
            '1989', '1990', '1991',
            '1992', '1993', '1994',
            '1995', '1996', '1997',
            '1998', '1999', '2000',
            '2001', '2002', '2003',
            '2004', '2005', '2006',
            '2007', '2008', '2009',
            '2010', '2011', '2012',
            '2013', '2014', '2015',
            '2016', '2017', '2018',
            '2019', '2020', '2021',
        ]
month=['01','02', '03', '04','05','06', '07', '08','09','10', '11','12',]
time=['00:00']

# Set to 1 (or any nonzero value) if required to clip and 0 to not clip
clp=0;
output_fn='/home/ritu/Desktop/FieldPrep/DataDownload/era5l_ns_mon_all_time.nc'

## User defined segment ends

## Download data
c = cdsapi.Client()

c.retrieve(
    dat_name,
    {
        'format': format,
        'variable': var_list,
        'year': year,
        'month': month,
        'time': time,
        'area': aoi,
    },
    'era5l_tp_19_20_JJAS.nc')

## Clip data to ROI as specified by user
if clp:
    dataset=xr.open_mfdataset('*.nc',decode_coords={'all'})
    dataset.rio.write_crs(shp.crs,inplace=True)
    clipped=dataset.rio.clip(shp.geometry,shp.crs,all_touched=True)
    os.remove('*.nc')
    clipped.to_netcdf(output_fn)