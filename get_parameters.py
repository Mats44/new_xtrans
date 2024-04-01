# Imports
import numpy as np
import pandas as pd
from read_materials_param import read_materials_param

def custom_len(item):
    # Check if the item is a number (int or float) or a non-variable string
    if isinstance(item, (int, float, str)):
        return 1
    else:
        # Return the length of the item
        return len(item)

def get_parameters(filename):
    """
    Reads in a transducer structure file and extracts the material parameters for different layers.
    
    Args:
        filename (str): The path to the transducer structure file.
        
    Returns:
        tuple: A tuple containing the materials data as a DataFrame and a dictionary of parameters.
    """
    # Initiating frequency vector and center frequency. All in [Hz].
    #fmin = user_input.fmin * 1e6 #this must be restricted by a minimum of df. It can't ever be zero #TODO
    #fmax = user_input.fmax * 1e6 #must be restricted to be larger than fmin. #TODO

    # f_min = 1 * 1e6 #TODO REPLACE BY USER INPUT. MINIMUM df.
    # f_max = 20 * 1e6 #TODO REPLACE BY USER INPUT. MINIMUM 2*df.
    # f = np.linspace(f_min, f_max, 1901, endpoint=True)
    df = 0.01e6  # The step size
    f_min = df
    f_min = 1e6
    f_max = 20e6 
    f = np.arange(f_min, f_max + df, df)
    
    f_c = 3 * 1e6
    len_f = len(f)
    w = 2 * np.pi * f

    # Read in transducer structure file to get material parameters
    materials_data = read_materials_param(filename) 

    # Find indexes for load, piezo, backing
    backing_index = materials_data.index[1] #the first row of df
    piezo_index = materials_data[materials_data['h[10^9 V/m]'].notna()].index[0] #piezo = k not zero
    load_index = materials_data.index[-1] #the last row of df

    # Extract parameters for the load
    load_params = materials_data.loc[load_index].iloc[1:]
    mat_load = load_params['Materials']
    c_load = load_params['c[m/s]']
    z_c_load = load_params['z_c[MRayl]'] * 1e6  # convert [MRayl] to [Rayl]
    d_load = load_params['d[mm]'] / 1000  # convert from [mm] to [meter]
    q_load = load_params['Q_m']

    # Extract parameters for front matching layers
    front_layers_params = materials_data.iloc[piezo_index+2:load_index-1]
    front_layers_params = front_layers_params.drop(front_layers_params.columns[0], axis=1)
    front_layers_params = front_layers_params.reset_index(drop=True)
    mat_front_layers = front_layers_params['Materials']
    c_front_layers = front_layers_params['c[m/s]']
    z_c_front_layers = front_layers_params['z_c[MRayl]'] * 1e6
    d_front_layers = front_layers_params['d[mm]'] / 1000
    q_front_layers = front_layers_params['Q_m']

    # Extract pzt parameters
    piezo_params = materials_data.loc[piezo_index].iloc[1:]
    mat_piezo = piezo_params['Materials']
    c_piezo = piezo_params['c[m/s]']
    z_c_piezo = piezo_params['z_c[MRayl]'] * 1e6
    d_piezo = piezo_params['d[mm]'] / 1000
    h_piezo = piezo_params['h[10^9 V/m]'] * 1e9
    q_piezo = piezo_params['Q_m']
    eps_r_piezo = piezo_params['eps_r']

    # Extract parameters from back matching layers
    back_layers_params = materials_data[(materials_data.index > backing_index+1) & 
                                        (materials_data.index < piezo_index-1)
                                        ]
    back_layers_params = back_layers_params[::-1] #reverse order of rows. Index [0] next to piezo
    back_layers_params = back_layers_params.reset_index(drop=True)
    mat_back_layers = back_layers_params['Materials']
    c_back_layers = back_layers_params['c[m/s]']
    z_c_back_layers = back_layers_params['z_c[MRayl]'] * 1e6
    d_back_layers = back_layers_params['d[mm]'] / 1000
    q_back_layers = back_layers_params['Q_m']

    # Extract parameters for backing
    backing_params = materials_data.loc[backing_index].iloc[1:]
    mat_backing = backing_params['Materials']
    c_backing = backing_params['c[m/s]']
    z_c_backing = backing_params['z_c[MRayl]'] * 1e6
    d_backing = backing_params['d[mm]'] / 1000
    q_backing = backing_params['Q_m']

    # Counting the various layers
    # Returns lenght of list, or '1' if a constant
    len_load = custom_len(z_c_back_layers)
    len_front_layers = custom_len(z_c_front_layers)
    len_piezo = custom_len(z_c_piezo)
    len_back_layers = custom_len(z_c_back_layers)
    len_backing = custom_len(z_c_backing)
    len_layers = (len_load + len_front_layers + len_piezo + 
                    len_back_layers + len_backing) #total nr of layers

    layer_counts = {
    'len_load': len_load,
    'len_front_layers': len_front_layers,
    'len_piezo': len_piezo,
    'len_back_layers': len_back_layers,
    'len_backing': len_backing,
    'len_layers': len_layers
    }

    column_labels = materials_data.columns.tolist() #column headers from dataframe as list
    z_elport_termination = np.ones((len_piezo, 1)) #initiate termination impedance

    # Final parameter dictionary
    params_dict = {
        'f': f,
        'len_f': len_f,
        'f_min': f_min,
        'f_max': f_max,
        'f_c': f_c,
        'w': w,
        'load': load_params,
        'front_layers': front_layers_params,
        'piezo': piezo_params,
        'back_layers': back_layers_params,
        'backing': backing_params,
        'layer_counts': layer_counts, #dict containing the count of the different layer types
        'column_labels': column_labels,
        'z_elport_termination': z_elport_termination,
        'c_load': c_load,
        'z_c_load': z_c_load,
        'd_load': d_load,
        'q_load': q_load,
        'c_front_layers': c_front_layers,
        'z_c_front_layers': z_c_front_layers,
        'd_front_layers': d_front_layers,
        'q_front_layers': q_front_layers,
        'c_piezo': c_piezo,
        'z_c_piezo': z_c_piezo,
        'd_piezo': d_piezo,
        'h_piezo': h_piezo,
        'q_piezo': q_piezo,
        'eps_r_piezo': eps_r_piezo,
        'c_back_layers': c_back_layers,
        'z_c_back_layers': z_c_back_layers,
        'd_back_layers': d_back_layers,
        'q_back_layers': q_back_layers,
        'c_backing': c_backing,
        'z_c_backing': z_c_backing,
        'd_backing': d_backing,
        'q_backing': q_backing
    }

    return materials_data, params_dict


def param_dict_extract(parameter_dict):
    '''
    Extracts all the variables from the parameter_dict.
    Returns all variables except main structure section variables.
    '''

    # ==================================
    # Extracting from dictionary
    # ==================================

    # Extracting frequency variables in [Hz]
    f = parameter_dict['f']
    f_min = parameter_dict['f_min']
    f_max = parameter_dict['f_max']
    f_c = parameter_dict['f_c']
    w = parameter_dict['w']

    # Assorted variables
    column_labels = parameter_dict['column_labels']
    z_elport_termination = parameter_dict['z_elport_termination']

    # Extracting the nested 'layer_counts' dictionary
    len_load = parameter_dict['layer_counts']['len_load'] #nr of loads
    len_front_layers = parameter_dict['layer_counts']['len_front_layers'] #nr of front layers
    len_piezo = parameter_dict['layer_counts']['len_piezo'] #nr of piezo layers
    len_back_layers = parameter_dict['layer_counts']['len_back_layers'] #nr of back layers
    len_backing = parameter_dict['layer_counts']['len_backing'] #nr of backings
    len_layers = parameter_dict['layer_counts']['len_layers'] #total nr of structure layers
    len_f = parameter_dict['len_f']

    # Extracting the parameters for all the parts of the structure
    load_params = parameter_dict['load']
    front_layers_params = parameter_dict['front_layers']
    piezo_params = parameter_dict['piezo']
    back_layers_params = parameter_dict['back_layers']
    backing_params = parameter_dict['backing']

    c_load = parameter_dict['c_load']
    z_c_load = parameter_dict['z_c_load']
    d_load = parameter_dict['d_load']
    q_load = parameter_dict['q_load']

    c_front_layers = parameter_dict['c_front_layers']
    z_c_front_layers = parameter_dict['z_c_front_layers']
    d_front_layers = parameter_dict['d_front_layers']
    q_front_layers = parameter_dict['q_front_layers']

    c_piezo = parameter_dict['c_piezo']
    z_c_piezo = parameter_dict['z_c_piezo']
    d_piezo = parameter_dict['d_piezo']
    h = parameter_dict['h_piezo']
    eps_r = parameter_dict['eps_r_piezo']
    q_piezo = parameter_dict['q_piezo']

    c_back_layers = parameter_dict['c_back_layers']
    z_c_back_layers = parameter_dict['z_c_back_layers']
    d_back_layers = parameter_dict['d_back_layers']
    q_back_layers = parameter_dict['q_back_layers']

    c_backing = parameter_dict['c_backing']
    z_c_backing = parameter_dict['z_c_backing']
    d_backing = parameter_dict['d_backing']
    q_backing = parameter_dict['q_backing']

    return (
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
