#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==============================================================================
# author          :Ghislain Vieilledent
# email           :ghislain.vieilledent@cirad.fr, ghislainv@gmail.com
# web             :https://ecology.ghislainv.fr
# python_version  :>=2.7
# license         :GPLv3
# ==============================================================================

#!/usr/bin/env python
# coding: utf-8

# # ForastAtRisk Tropics
# 
# This notebook provides a minimal and reproducible example for the following scientific article:
# 
# **Vieilledent G., C. Vancutsem, and F. Achard.** Spatial forecasting of forest cover change in the humid tropics over the 21st century.
# 
# We use the [Guadeloupe](https://en.wikipedia.org/wiki/Guadeloupe) archipelago as a case study.

import os

import numpy as np
import pandas

def test_make_dir():
    assert os.path.exists("output")


def test_data():
    assert os.path.exists("data")


def test_plot_fcc23():
    assert os.path.exists("output/fcc23.png")


def test_sample():
    assert os.path.exists("output/sample.txt")


def test_sample(gstart):
    assert gstart["dataset"].iloc[0, 0] == 30.0


def test_cellneigh(gstart):
    a = np.array([3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5,
                  5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5,
                  5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5,
                  5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5,
                  3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3])
    b = np.array([ 1, 11, 12,  0,  2, 11, 12, 13,  1,  3, 12, 13, 14,  2,  4, 13, 14,
                   15,  3,  5, 14, 15, 16,  4,  6, 15, 16, 17,  5,  7, 16, 17, 18,  6,
                   8, 17, 18, 19,  7,  9, 18, 19, 20,  8, 10, 19, 20, 21,  9, 20, 21,
                   0,  1, 12, 22, 23,  0,  1,  2, 11, 13, 22, 23, 24,  1,  2,  3, 12,
                   14, 23, 24, 25,  2,  3,  4, 13, 15, 24, 25, 26,  3,  4,  5, 14, 16,
                   25, 26, 27,  4,  5,  6, 15, 17, 26, 27, 28,  5,  6,  7, 16, 18, 27,
                   28, 29,  6,  7,  8, 17, 19, 28, 29, 30,  7,  8,  9, 18, 20, 29, 30,
                   31,  8,  9, 10, 19, 21, 30, 31, 32,  9, 10, 20, 31, 32, 11, 12, 23,
                   33, 34, 11, 12, 13, 22, 24, 33, 34, 35, 12, 13, 14, 23, 25, 34, 35,
                   36, 13, 14, 15, 24, 26, 35, 36, 37, 14, 15, 16, 25, 27, 36, 37, 38,
                   15, 16, 17, 26, 28, 37, 38, 39, 16, 17, 18, 27, 29, 38, 39, 40, 17,
                   18, 19, 28, 30, 39, 40, 41, 18, 19, 20, 29, 31, 40, 41, 42, 19, 20,
                   21, 30, 32, 41, 42, 43, 20, 21, 31, 42, 43, 22, 23, 34, 44, 45, 22,
                   23, 24, 33, 35, 44, 45, 46, 23, 24, 25, 34, 36, 45, 46, 47, 24, 25,
                   26, 35, 37, 46, 47, 48, 25, 26, 27, 36, 38, 47, 48, 49, 26, 27, 28,
                   37, 39, 48, 49, 50, 27, 28, 29, 38, 40, 49, 50, 51, 28, 29, 30, 39,
                   41, 50, 51, 52, 29, 30, 31, 40, 42, 51, 52, 53, 30, 31, 32, 41, 43,
                   52, 53, 54, 31, 32, 42, 53, 54, 33, 34, 45, 55, 56, 33, 34, 35, 44,
                   46, 55, 56, 57, 34, 35, 36, 45, 47, 56, 57, 58, 35, 36, 37, 46, 48,
                   57, 58, 59, 36, 37, 38, 47, 49, 58, 59, 60, 37, 38, 39, 48, 50, 59,
                   60, 61, 38, 39, 40, 49, 51, 60, 61, 62, 39, 40, 41, 50, 52, 61, 62,
                   63, 40, 41, 42, 51, 53, 62, 63, 64, 41, 42, 43, 52, 54, 63, 64, 65,
                   42, 43, 53, 64, 65, 44, 45, 56, 66, 67, 44, 45, 46, 55, 57, 66, 67,
                   68, 45, 46, 47, 56, 58, 67, 68, 69, 46, 47, 48, 57, 59, 68, 69, 70,
                   47, 48, 49, 58, 60, 69, 70, 71, 48, 49, 50, 59, 61, 70, 71, 72, 49,
                   50, 51, 60, 62, 71, 72, 73, 50, 51, 52, 61, 63, 72, 73, 74, 51, 52,
                   53, 62, 64, 73, 74, 75, 52, 53, 54, 63, 65, 74, 75, 76, 53, 54, 64,
                   75, 76, 55, 56, 67, 77, 78, 55, 56, 57, 66, 68, 77, 78, 79, 56, 57,
                   58, 67, 69, 78, 79, 80, 57, 58, 59, 68, 70, 79, 80, 81, 58, 59, 60,
                   69, 71, 80, 81, 82, 59, 60, 61, 70, 72, 81, 82, 83, 60, 61, 62, 71,
                   73, 82, 83, 84, 61, 62, 63, 72, 74, 83, 84, 85, 62, 63, 64, 73, 75,
                   84, 85, 86, 63, 64, 65, 74, 76, 85, 86, 87, 64, 65, 75, 86, 87, 66,
                   67, 78, 88, 89, 66, 67, 68, 77, 79, 88, 89, 90, 67, 68, 69, 78, 80,
                   89, 90, 91, 68, 69, 70, 79, 81, 90, 91, 92, 69, 70, 71, 80, 82, 91,
                   92, 93, 70, 71, 72, 81, 83, 92, 93, 94, 71, 72, 73, 82, 84, 93, 94,
                   95, 72, 73, 74, 83, 85, 94, 95, 96, 73, 74, 75, 84, 86, 95, 96, 97,
                   74, 75, 76, 85, 87, 96, 97, 98, 75, 76, 86, 97, 98, 77, 78, 89, 77,
                   78, 79, 88, 90, 78, 79, 80, 89, 91, 79, 80, 81, 90, 92, 80, 81, 82,
                   91, 93, 81, 82, 83, 92, 94, 82, 83, 84, 93, 95, 83, 84, 85, 94, 96,
                   84, 85, 86, 95, 97, 85, 86, 87, 96, 98, 86, 87, 97])
    assert (np.array_equal(gstart["nneigh"], a) and np.array_equal(gstart["adj"], b))


def test_model_binomial_iCAR(gstart):
    p = np.array([0.34388896, 0.29002158, 0.51594223, 0.48436339, 0.60838453,
                  0.61257058, 0.55034979, 0.58819568, 0.51087469, 0.58819568,
                  0.64149789, 0.57400436, 0.59570952, 0.63212285, 0.566676  ,
                  0.62562204, 0.55379459, 0.15644965, 0.61284327, 0.36638686,
                  0.55439297, 0.57325744, 0.62562204, 0.17995823, 0.4930868 ,
                  0.54641479, 0.59782004, 0.48159526, 0.62882886, 0.59831051,
                  0.76245777, 0.74576097, 0.77356767, 0.73863295, 0.78188891,
                  0.75056545, 0.60775752, 0.64978574, 0.74654465, 0.77378323,
                  0.53994416, 0.75852715, 0.77754366, 0.60053684, 0.71543739,
                  0.74565542, 0.7555028 , 0.44598923, 0.76401273, 0.75953027,
                  0.49027142, 0.69610182, 0.75679461, 0.78543649, 0.76863321,
                  0.6209473 , 0.77653139, 0.76182804, 0.78169681, 0.58816002,
                  0.50453473, 0.77980428, 0.76084413, 0.73054832, 0.78289747,
                  0.71858934, 0.78362842, 0.74702923, 0.67357571, 0.78940242,
                  0.75358937, 0.66791346, 0.75602843, 0.42494845, 0.77653139,
                  0.60509306, 0.60846943, 0.76187008, 0.73278992, 0.72792572,
                  0.47661681, 0.59456417, 0.71894598, 0.6731302 , 0.74964489,
                  0.77247818, 0.78289747, 0.74200682, 0.78940242, 0.78508877,
                  0.73153419, 0.65636031, 0.78607775, 0.59738545, 0.72596162,
                  0.78216462, 0.75078253, 0.77527468, 0.69907386, 0.71991522])
    assert np.allclose(gstart["pred_icar"][0:100], p)


def test_rho(gstart):
    r = np.array([-3.72569484e-02, -1.16871478e-01, -1.82400711e-01,  2.13446770e-01,
                  -6.44591325e-01, -9.89850864e-02,  1.10439030e-01, -2.31551563e-02,
                  -3.30273946e-01, -2.66995061e-01, -3.84426210e-01,  5.73572517e-02,
                  -5.73353804e-02, -3.12497338e-01, -8.37127591e-01,  7.62072575e-02,
                  3.86361945e-01,  1.26487021e-02, -8.22069815e-02, -3.60656850e-01,
                  -5.46586761e-01, -4.17346094e-01,  1.05212875e+00, -4.32508096e-02,
                  -4.49589533e-01, -6.89872259e-01, -4.91230799e-01, -3.84040358e-01,
                  5.67299746e-01, -2.10071117e-01, -1.07456253e+00, -6.69339978e-01,
                  -6.21974970e-01,  2.15020267e+00, -7.16437085e-02, -4.46424607e-01,
                  -2.17259138e-01, -3.30043032e-01, -2.59613996e-01,  2.68845283e-01,
                  -3.78046974e-01, -5.18108829e-01, -6.18235133e-01, -7.59652734e-01,
                  1.51771355e+00,  1.75357016e+00, -8.01814048e-02,  1.99270623e-01,
                  -1.75157345e-01, -6.10561635e-02, -1.26099802e-01, -1.77864133e-01,
                  -3.03381214e-01, -5.29892286e-01, -5.47125418e-01,  1.30320979e+00,
                  2.37670385e+00,  4.97829325e-01,  8.88668246e-01,  3.92682659e-01,
                  -6.56913949e-03, -2.95774565e-01, -5.15489012e-01, -6.01407176e-01,
                  -5.67695385e-01, -6.48479745e-01,  1.47482553e+00,  1.45848019e+00,
                  4.05321503e-01,  1.06327906e+00,  4.37780456e-01, -1.12202021e-01,
                  -7.22139489e-01, -7.33312519e-01, -6.68442058e-01, -7.76218335e-01,
                  -8.02763852e-01,  1.41620727e+00,  1.56564133e+00,  1.24252305e+00,
                  9.07095194e-01,  4.38959947e-01, -2.95546782e-01, -4.92024764e-01,
                  -9.62965263e-01, -8.93107795e-01, -9.80673724e-01, -9.94878624e-01,
                  1.41460696e+00,  1.38942057e+00,  1.97092977e+00,  1.06797639e+00,
                  4.36803818e-01,  2.15296806e-03, -6.14110567e-01, -7.76157636e-01,
                  -9.47693103e-01, -1.05424592e+00, -1.12226096e+00])
    assert np.allclose(gstart["rho"], r)


def test_interpolate_rho():
    assert os.path.exists("output/rho.tif")


def test_predict_raster_binomial_iCAR():
    assert os.path.exists("output/prob.tif")


def test_countpix(gstart):
    assert gstart["fc"] == [83999.25, 79015.5]


def test_deforest():
    assert os.path.exists("output/fcc_2050.tif")


def test_plot_fcc123():
    assert os.path.exists("output/fcc123.png")


def test_plot_rho():
    assert os.path.exists("output/rho_orig.png")


def test_plot_prob():
    assert os.path.exists("output/prob.png")


def test_plot_fcc():
    assert os.path.exists("output/fcc_2050.png")


# End Of File