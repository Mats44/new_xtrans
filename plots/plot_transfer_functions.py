import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from get_parameters import param_dict_extract

def plot_transfer_functions(Y_tt, coupling, f, parameter_dict):
    
    (
        (
            f,
            f_min,
            f_max,
            f_c,
            w,
            column_labels,
            z_elport_termination,
            len_load,
            len_front_layers,
            len_piezo,
            len_back_layers,
            len_backing,
            len_layers,
            len_f,
            load_params,
            front_layers_params,
            piezo_params,
            back_layers_params,
            backing_params,
            c_load,
            z_c_load,
            d_load,
            q_load,
            c_front_layers,
            z_c_front_layers,
            d_front_layers,
            q_front_layers,
            c_piezo,
            z_c_piezo,
            d_piezo,
            h,
            eps_r,
            q_piezo,
            c_back_layers,
            z_c_back_layers,
            d_back_layers,
            q_back_layers,
            c_backing,
            z_c_backing,
            d_backing,
            q_backing,
        )
    ) = param_dict_extract(parameter_dict)
        
    coupling = 1 # temp manually selected value of either 0 or 1
    
    H_tt = np.zeros((1, len_f))
    
    if coupling == 1:
        
        H_tt = H_tt
    
    else:
        
        H_tt = comp_Htt_layer(sXtrans_data).' # = H_tt ??