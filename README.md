# aliens-unmix-emit
Unmixing alien vegetation in fynbos using EMIT surface reflectance

__under constuction__

This code performs spectral unmixing on imaging spectroscopy surface relfectance data from the [Earth Surface Mineral Dust Source Investigation (EMIT) mission](https://earth.jpl.nasa.gov/emit/). Currently, EMIT data need to be downloaded locally beforehand from [LP DAAC](https://search.earthdata.nasa.gov/search?q=emit). Unmixing is performed using the [SpectralUnmixing](https://github.com/emit-sds/SpectralUnmixing) Julia package provided by the EMIT science team, hence this code requires both Julia==1.6.5 and Python>=3.8

The example provided in this repo attempts to unmix water, bareground/rock, native vegetation and invasive Pine trees endmembers in the southwestern Cape of South Africa

## Install
```
git clone git@github.com:GMoncrieff/aliens-unmix-emit.git
pip install --editable git@github.com:GMoncrieff/aliens-unmix-emit.git
```

make sure the following files are present in your data/ folder:  
- the emit reflectance netcdf.  
e.g. EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc. 
- labelled points for extraction of endmembers.  
e.g. sample_coords_long.csv.  
an example is provided in [data/sample_coords_long.csv](data/sample_coords_long.csv). 

## Install externals tools

Install emit-utils
```
cd aliens-unmix-emit
git clone git@github.com:emit-sds/emit-utils.git
pip install --editable git@github.com:emit-sds/emit-utils.git
```

Install SpectralUnmixing (requires Julia 1.6.5)
```
git clone git@github.com:emit-sds/SpectralUnmixing.git
cd SpectralUnmixing
julia -e 'using Pkg; Pkg.activate("."); Pkg.precompile()'
export JULIA_PROJECT=${PWD}
cd ..
```

## Execute script
You will probably want to edit file paths inside this file before doing this
```
chmod +x reformat_unmix.sh
./reformat_unmix.sh
```

view some results [here](https://glennwithtwons.users.earthengine.app/view/emit-unmix-test)

