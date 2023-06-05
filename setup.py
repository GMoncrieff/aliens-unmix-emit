"""
Core utility package to support EMIT data processing.

Author: Glenn R. Moncrieff, glenn@saeon.ac.za
"""

from setuptools import setup, find_packages

setup(name='emit_utils',
      packages=find_packages(),
      include_package_data=True,
      version='1.0.0',
      install_requires=[
          'gdal>=2.0',
          'spectral>=0.21',
          'numpy>=1.19.2',
          'netcdf4>=1.5.8',
          'argparse>=1.0',
          'pandas>=1.2.0',
          'xarray>=0.17.0',
          'rioxarray>=0.10.0',
          'geopandas>=0.10.0',
      ],
      python_requires='>=3.8',
      platforms='any',
      classifiers=['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent'])