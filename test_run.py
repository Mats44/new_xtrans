from get_parameters import get_parameters
from plots.plot_electrical_imp import plot_electrical_imp
from plots.plot_transfer_functions import plot_transfer_functions
from transfer_functions import admittance

#### Get variables ####
#struct_filename = "struct_0front_0back_air_air.xlsx"
#struct_filename = "struct_1front_0back_air_air.xlsx"
#struct_filename = "struct_1front_0back_air_water.xlsx"
#struct_filename = "struct_1front_1back_water_air.xlsx"
#struct_filename = "struct_1front_2back_water_air.xlsx"
#struct_filename = "struct_2front_0back_air_air.xlsx"
#struct_filename = "struct_2front_0back_water_air.xlsx"
struct_filename = "struct_2front_1back_water_air.xlsx"
#struct_filename = "struct_3front_0back_water_air.xlsx"
#struct_filename = "struct_3front_1back_water_air.xlsx"    
#struct_filename = "struct_3front_3back_water_air.xlsx"

#struct_filename = "struct_0front_1back_water_air.xlsx"
#struct_filename = "struct_0front_3back_water_air.xlsx"

materials_data, parameter_dict = get_parameters(struct_filename)
Y_el, h_tt, f, unit_area = admittance(parameter_dict)

coupling = 1

#plot_electrical_imp(Y_el, f)
plot_transfer_functions(h_tt, coupling, f, parameter_dict)