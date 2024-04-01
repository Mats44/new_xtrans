# Install requirements
# %pip install matplotlib, numpy, pandas, openpyxl
# pip install requirements.txt

# Standard library imports
import os
import sys

# Third-party library imports


# Module imports from local application
from get_parameters import get_parameters
# from admittance_xtrans import admittance
from mechanical_impedance import mechanical_impedance
from plots.plot_mech_imp import plot_mech_imp
from plots.plot_mech_imp_matplotlib import plot_mech_imp_matplotlib
from transfer_functions import admittance

# Get variables
struct_filename = "struct_params_1back_3front_air_water.xlsx"  # name of file in 'new_xtrans/parameters/'
materials_data, parameter_dict = get_parameters(
    struct_filename
)  # a dictionary of parameters

# Mechanical Impedance
z_load_to_backing, z_backing_to_load = mechanical_impedance(parameter_dict)
plot_mech_imp_matplotlib(z_load_to_backing, z_backing_to_load, parameter_dict)

# Transfer Functions
transfer_functions = admittance(parameter_dict, z_load_to_backing, z_backing_to_load)
