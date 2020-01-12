#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
# author          :Ghislain Vieilledent
# email           :ghislain.vieilledent@cirad.fr, ghislainv@gmail.com
# web             :https://ecology.ghislainv.fr
# python_version  :>=2.7
# license         :GPLv3
# ==============================================================================

# Import
from __future__ import division, print_function  # Python 3 compatibility
import os
import numpy as np
from osgeo import gdal


# wrast_rho
def wrast_rho(rho, input_raster, csize=10, output_file="output/rho_orig.tif"):
    """Write rho values to GeoTIFF.

    This function writes rho values (spatial random effects) to a
    GeoTIFF raster file.

    :param rho: original rho values estimates with the iCAR model.
    :param input_raster: path to input raster defining the region.
    :csize: size of the spatial cells (in km).
    :output_file: path to output raster file.

    """

    # Region
    r = gdal.Open(input_raster)
    ncol = r.RasterXSize
    nrow = r.RasterYSize
    gt = r.GetGeoTransform()
    xres = gt[1]
    yres = -gt[5]
    Xmin = gt[0]
    Xmax = gt[0] + xres * ncol
    Ymin = gt[3] - yres * nrow
    Ymax = gt[3]

    # Cell number from region
    csize_orig = csize_orig * 1000  # Transform km in m
    ncell_X = int(np.ceil((Xmax - Xmin) / csize_orig))
    ncell_Y = int(np.ceil((Ymax - Ymin) / csize_orig))

    # NumpyArray
    rho = np.array(rho)
    rho_arr = rho.reshape(ncell_Y, ncell_X)

    # Create .tif file
    dirname = os.path.dirname(output_file)
    rho_orig_filename = os.path.join(dirname, "rho_orig.tif")
    driver = gdal.GetDriverByName("GTiff")
    rho_R = driver.Create(rho_orig_filename, ncell_X, ncell_Y, 1,
                          gdal.GDT_Float64)
    rho_R.SetProjection(r.GetProjection())
    gt = list(gt)
    gt[1] = csize_orig
    gt[5] = -csize_orig
    rho_R.SetGeoTransform(gt)

    # Write data
    print("Write spatial random effect data to disk")
    rho_B = rho_R.GetRasterBand(1)
    rho_B.WriteArray(rho_arr)
    rho_B.FlushCache()
    rho_B.SetNoDataValue(-9999)

    # Compute statistics
    print("Compute statistics")
    rho_B.FlushCache()  # Write cache data to disk
    rho_B.ComputeStatistics(False)

    # Build overviews
    print("Build overview")
    rho_R.BuildOverviews("average", [2, 4, 8, 16, 32])

    # Dereference driver
    rho_B = None
    del rho_R

# End
