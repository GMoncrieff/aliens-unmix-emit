#mamba activate gis

echo "create spectral library"
python extract_spectra.py /home/glenn/emit/ \
    data/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc \
    data/sample_coords_long.csv

echo "convert necdf to envi"
python emit_utils/emit_utils/reformat.py \
    data/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc \
    data

echo "unmix spectra"
cd SpectralUnmixing
julia -e 'using Pkg; Pkg.activate("."); Pkg.precompile()'
export JULIA_PROJECT=${PWD}
julia -p 8 unmix.jl /home/glenn/emit/data/EMIT_L2A_RFL_001_20230119T114247_2301907_005_reflectance /home/glenn/emit/data/example_lib.csv Category mesma_test --num_endmembers 4 --mode mesma

echo "orthorectify convert to cog"
python clean_unmix.py /home/glenn/emit/ \
    data/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc \
    SpectralUnmixing/mesma_test_fractional_cover \
    mask