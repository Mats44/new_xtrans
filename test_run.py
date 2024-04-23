from get_parameters import get_parameters
from plots.plot_electrical_imp import plot_electrical_imp
from transfer_functions import admittance

#struct_filename = "struct_1front_0back_air_water.xlsx"
#struct_filename = "struct_1front_0back_air_air.xlsx"
#struct_filename = "struct_params_0back_0front_air_air.xlsx"
struct_filename = "struct_3front_1back_water_air.xlsx"
#struct_filename = "testing_3front_3back_air_water.xlsx"

materials_data, parameter_dict = get_parameters(struct_filename)

Y_el, h_tt, f, unit_area = admittance(parameter_dict)
plot_electrical_imp(Y_el, f)