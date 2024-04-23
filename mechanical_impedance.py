# Imports
import numpy as np
from get_parameters import param_dict_extract

def piezo_mech_imp(z_in, len_piezo, len_f, z_c_piezo, kd_piezo):
    """
    Calculates mechanical impedance of the piezo layer as seen from load towards backing.
    """
    z_adjacent = np.copy(z_in)
    z_in_piezo = np.zeros((len_piezo, len_f), dtype=complex)
    
    ## A-matrix elements
    a_11_piezo = np.cos(kd_piezo)
    a_12_piezo = 1j * z_c_piezo * np.sin(kd_piezo)
    a_21_piezo = 1j * (1/z_c_piezo) * np.sin(kd_piezo)
    a_22_piezo = a_11_piezo

    ## Find piezo impedance
    z_in_piezo = ((a_11_piezo * z_adjacent[0, :] + a_12_piezo) /
                  (a_21_piezo * z_adjacent[0, :] + a_22_piezo)
                    )

    return z_in_piezo

def load_to_piezo(len_front_layers, len_f, z_c_front_layers, kd_front, z_c_load):
    """
    Calculates the impedance seen from the piezo layer in a transducer stack model.

    Returns:
        z_in_front: The impedance seen from the piezo layer.
    """

    if len_front_layers > 0:
        
        z_in_front = np.zeros((len_front_layers, len_f), dtype=complex)
        
        # A-matrix elements
        a_11_front = np.cos(kd_front)
        a_12_front = 1j * z_c_front_layers * np.sin(kd_front)
        a_21_front = 1j * (1/z_c_front_layers) * np.sin(kd_front)
        a_22_front = a_11_front
        
        for k in range(len_front_layers-1, -1, -1):
            if k == len_front_layers-1:
                ## First layer (interfacing load)
                z_in_front[k, :] = (
                    (a_11_front[-1, :] * z_c_load + a_12_front[-1, :])/
                    (a_21_front[-1, :] * z_c_load + a_22_front[-1, :])
                    )
            else:
                ## Remaining layers (final layer, index [0], interfaces with piezoceramic)
                z_in_front[k, :] = (
                    (a_11_front[k, :] * z_in_front[k+1, :] + a_12_front[k,:])/
                    (a_21_front[k, :] * z_in_front[k+1, :] + a_22_front[k, :])
                    )
                
    else:
        ## If there are no front layers, the impedance seen from the piezo is just the load impedance
        z_in_front = np.zeros((1, len_f), dtype=complex)
        z_in_front[0, :] = z_c_load

    return z_in_front

def piezo_to_backing(z_in_piezo, len_back_layers, len_f, z_c_back_layers, kd_back):
    """
    Calculates the mechanical impedance seen from piezo layer towards backing.

    Returns:
        z_in_back: The impedance seen from the backing.
    """
    
    ## Check if there are any back layers
    if len_back_layers > 0:
    
        z_in_back = np.zeros((len_back_layers, len_f), dtype=complex)
        
        ## A-matrix elements
        a_11_back = np.cos(kd_back)
        a_12_back = 1j * z_c_back_layers * np.sin(kd_back)
        a_21_back = 1j * (1/z_c_back_layers) * np.sin(kd_back)
        a_22_back = a_11_back
        
        for k in range(0, len_back_layers):
            if k == 0:
                ## First layer (interfacing piezo layer)
                z_in_back[k, :] = (
                    (a_11_back[k, :] * z_in_piezo + a_12_back[k, :])
                    / (a_21_back[k, :] * z_in_piezo + a_22_back[k, :])
                )
            else:
                ## Remaining layers (last layer, [-1], interfaces backing)
                z_in_back[k, :] = (
                    (a_11_back[k, :] * z_in_back[k-1, :] + a_12_back[k, :])
                    / (a_21_back[k, :] * z_in_back[k-1, :] + a_22_back[k, :])
                )
    else:
        ## If there are no back layers, the impedance seen from the backing is load + front layers + piezo. 
        ## No additional contribution from back layers --> return empty array
        
            # z_in_front = np.zeros((1, len_f), dtype=complex)
            # z_in_front[-1, :] = z_c_backing
            #z_in_back = np.empty((0, 0))
            z_in_back = np.empty((0, len_f), dtype=complex)
        
        
    return z_in_back

def backing_to_piezo(z_in_back_reverse, len_back_layers, len_f, z_c_back_layers, kd_back, z_c_backing):
    """
    Calculates the mechanical impedance seen from backing towards piezo layer.

    Returns:

    """
    # Check if there are any back layers
    if len_back_layers > 0:
        
        z_in_back_reverse = np.zeros((len_back_layers, len_f), dtype=complex)
        
        # A-matrix elements for back layers
        a_11_back_reverse = np.cos(kd_back)
        a_12_back_reverse = 1j * z_c_back_layers * np.sin(kd_back)
        a_21_back_reverse = 1j * (1/z_c_back_layers) * np.sin(kd_back)
        a_22_back_reverse = a_11_back_reverse

        for k in range(len_back_layers - 1, -1, -1):
            if k == len_back_layers - 1:
                # Last layer (interfacing backing)
                z_in_back_reverse[k, :] = (
                    (a_11_back_reverse[k, :] * z_c_backing + a_12_back_reverse[k, :]) /
                    (a_21_back_reverse[k, :] * z_c_backing + a_22_back_reverse[k, :])
                )
            else:
                # Remaining layers (first layer, index [0], interfaces piezo)
                z_in_back_reverse[k, :] = (
                    (a_11_back_reverse[k, :] * z_in_back_reverse[k+1, :] + a_12_back_reverse[k, :]) /
                    (a_21_back_reverse[k, :] * z_in_back_reverse[k+1, :] + a_22_back_reverse[k, :])
                )
    else:
        # If there are no back layers, the impedance seen from the piezo is just the backing impedance
        z_in_back_reverse = np.zeros((1, len_f), dtype=complex)
        z_in_back_reverse[0, :] = z_c_backing
        
    return z_in_back_reverse


def piezo_to_load(len_front_layers, len_f, z_c_front_layers, kd_front, z_in_piezo_reverse):
    """
    Calculates the mechanical impedance seen from piezo layer towards load.

    Returns:
        z_in_front_reverse (np.array): The impedance seen from the front in reverse order.
    """
    
    # Check if there are any front layers
    if len_front_layers > 0:

        z_in_front_reverse = np.zeros((len_front_layers, len_f), dtype=complex)
        
        # A-matrix elements for front layers      
        a_11_front_reverse = np.cos(kd_front) 
        a_12_front_reverse = 1j * z_c_front_layers * np.sin(kd_front)
        a_21_front_reverse = 1j * (1/z_c_front_layers) * np.sin(kd_front)
        a_22_front_reverse = a_11_front_reverse

        for k in range(0, len_front_layers):
            if k == 0:
                # First layer (interfacing piezo layer)
                z_in_front_reverse[k, :] = (
                    (a_11_front_reverse[k, :] * z_in_piezo_reverse + a_12_front_reverse[k, :]) /
                    (a_21_front_reverse[k, :] * z_in_piezo_reverse + a_22_front_reverse[k, :])
                )
            else:
                # Remaining layers (last layer, [-1], interfaces load)
                z_in_front_reverse[k, :] = (
                    (a_11_front_reverse[k, :] * z_in_front_reverse[k-1, :] + a_12_front_reverse[k, :]) /
                    (a_21_front_reverse[k, :] * z_in_front_reverse[k-1, :] + a_22_front_reverse[k, :])
                )
    else:
        # If there are no front layers, the impedance seen from the load is back layers + piezo impedance.
        # No additional contribution from back layers --> return empty array
        #z_in_front_reverse = np.empty((0, 0))
        z_in_front_reverse = np.empty((0, len_f), dtype=complex)
        
    return z_in_front_reverse   


def mechanical_impedance(parameter_dict):
    """
    Calculates the mechanical impedance of the piezoelectric stack
    """
    # ==================================
    # Extracting variables
    # ==================================

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

    # ==================================
    # Initiating variables
    # ==================================
    
    w = w.reshape(1, -1)  # Reshaping w to be a column vector

    # Converting from pandas series to 2D numpy array (for the sake of broadcasting)
    c_front_layers = c_front_layers.to_numpy().reshape(-1, 1)
    z_c_front_layers = z_c_front_layers.to_numpy().reshape(-1, 1)
    d_front_layers = d_front_layers.to_numpy().reshape(-1, 1)
    q_front_layers = q_front_layers.to_numpy().reshape(-1, 1)

    # c_piezo = np.array([[c_piezo]])
    # z_c_piezo = np.array([[z_c_piezo]])
    # d_piezo = np.array([[d_piezo]])
    # h = np.array([[h]])
    # eps_r = np.array([[eps_r]])

    c_back_layers = c_back_layers.to_numpy().reshape(-1, 1)
    z_c_back_layers = z_c_back_layers.to_numpy().reshape(-1, 1)
    d_back_layers = d_back_layers.to_numpy().reshape(-1, 1)
    q_back_layers = q_back_layers.to_numpy().reshape(-1, 1)

    # # Reciprocals of Q
    # q_load_rec = 1 / q_load
    # q_front_rec = 1 / q_front_layers
    # q_piezo_rec = np.array([[1 / q_piezo]])
    # q_back_rec = 1 / q_back_layers
    # q_backing_rec = 1 / q_backing

    #kd
    # kd_front = (1 - 0.5j * q_front_rec) * d_front_layers/c_front_layers * w
    # kd_back = (1 - 0.5j * q_back_rec) * d_back_layers/c_back_layers * w 
    # kd_piezo = (1 - 0.5j * q_piezo_rec) * (d_piezo / c_piezo) * w 

    if len_front_layers > 0:
        kd_front = d_front_layers/c_front_layers * w
    else:
        kd_front = np.zeros((1, len_f))
        
    if len_back_layers > 0:
        kd_back = d_back_layers/c_back_layers * w 
    else:
        kd_back = np.zeros((1, len_f))

    kd_piezo = d_piezo / c_piezo * w 

    # kd_piezo = kd_piezo.reshape(1, -1)

    # # Adding in Q loss
    # z_c_backing = z_c_backing * (1 + 0.5j * q_backing_rec)
    # z_c_back_layers = z_c_back_layers * (1 + 0.5j * q_back_rec)
    # z_c_piezo = z_c_piezo * (1 + 0.5j * q_piezo_rec)
    # z_c_front_layers = z_c_front_layers * (1 + 0.5j * q_front_rec)
    # z_c_load = z_c_load * (1 + 0.5j * q_load_rec)

    # # Correct dimensions of arrays for broadcasting
    # z_c_load = z_c_load * np.ones((1, len_f))
    # z_c_piezo = z_c_piezo * np.ones((1, len_f))
    # z_c_front_layers = z_c_front_layers * np.ones((1, len_f))
    # z_c_back_layers = z_c_back_layers * np.ones((1, len_f))
    # z_c_backing = z_c_backing * np.ones((1, len_f))

    # ==================================
    # Calculate impedance from load to the layer interfacing the backing
    # ==================================

    # calculate impedance from load to piezo layer
    z_in_front = load_to_piezo(len_front_layers, len_f, z_c_front_layers, kd_front, z_c_load) 
    
    # calculate impedance in piezo layer, going from front face to back face
    z_in_piezo = piezo_mech_imp(z_in_front, len_piezo, len_f, z_c_piezo, kd_piezo)

    # calculate impedance from piezo layer to backing
    z_in_back = piezo_to_backing(z_in_piezo, len_back_layers, len_f, z_c_back_layers, kd_back)

    # stack the arrays
    if z_in_front.size > 0 and z_in_back.size > 0: # [0] = Layer interfacing load, [-1] = Layer interfacing backing, [len_front_layers-1] = Piezo layer
        z_load_to_backing = np.vstack([z_in_front, z_in_piezo, z_in_back])
    elif z_in_front.size > 0 and z_in_back.size == 0: # [0] = layer interfacing load, [-1] = piezo layer
        z_load_to_backing = np.vstack([z_in_front, z_in_piezo])
    elif z_in_front.size == 0 and z_in_back.size > 0: # [0] = piezo layer, [-1] = layer interfacing backing
        z_load_to_backing = np.vstack([z_in_piezo, z_in_back])
    elif z_in_front.size == 0 and z_in_back.size == 0:
        z_load_to_backing = z_in_piezo

    # ==================================
    # Calculate impedance from backing to the layer interfacing the load
    # ==================================

    # calculate impedance from backing to piezo layer
    z_in_back_reverse = backing_to_piezo(z_in_back, len_back_layers, len_f, z_c_back_layers, kd_back, z_c_backing)

    # calculate impedance in piezo layer, going from back face (z_in_back_reverse) to front face
    z_in_piezo_reverse = piezo_mech_imp(z_in_back_reverse, len_piezo, len_f, z_c_piezo, kd_piezo)

    # calculate impedance from piezo layer to load
    z_in_front_reverse = piezo_to_load(len_front_layers, len_f, z_c_front_layers, kd_front, z_in_piezo_reverse)

    # Stack the arrays in reverse order
    if z_in_back_reverse.size > 0 and z_in_front_reverse.size > 0: # [0] = Layer interfacing backing, [-1] = Layer interfacing load, [len_back_layers-1] = Piezo layer
        z_backing_to_load = np.vstack([z_in_back_reverse, z_in_piezo_reverse, z_in_front_reverse])
    elif z_in_back_reverse.size > 0 and z_in_front_reverse.size == 0: # [0] = layer interfacing backing, [-1] = piezo layer
        z_backing_to_load = np.vstack([z_in_back_reverse, z_in_piezo_reverse])
    elif z_in_back_reverse.size == 0 and z_in_front_reverse.size > 0: # [0] = piezo layer, [-1] = layer interfacing load
        z_backing_to_load = np.vstack([z_in_piezo_reverse, z_in_front_reverse])
    elif z_in_back_reverse.size == 0 and z_in_front_reverse.size == 0:
        z_backing_to_load = z_in_piezo_reverse

    return z_load_to_backing, z_backing_to_load, z_in_front, z_in_piezo, z_in_back, z_in_back_reverse, z_in_piezo_reverse, z_in_front_reverse

##################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from get_parameters import get_parameters
    from plots.plot_mech_imp_matplotlib import plot_mech_imp_matplotlib

    #struct_filename = "struct_1front_0back_air_water.xlsx"
    #struct_filename = "struct_1front_0back_air_air.xlsx"
    #struct_filename = "struct_params_0back_0front_air_air.xlsx"
    struct_filename = "struct_3front_1back_water_air.xlsx"
    #struct_filename = "testing_3front_3back_air_water.xlsx"

    materials_data, parameter_dict = get_parameters(struct_filename)

    (
        z_load_to_backing,
        z_backing_to_load,
        z_in_front,
        z_in_piezo,
        z_in_back,
        z_in_back_reverse,
        z_in_piezo_reverse,
        z_in_front_reverse
    ) = mechanical_impedance(parameter_dict)

    plot_mech_imp_matplotlib(
        z_load_to_backing,
        z_backing_to_load,
        z_in_front,
        z_in_piezo,
        z_in_back,
        z_in_back_reverse,
        z_in_piezo_reverse,
        z_in_front_reverse,
        parameter_dict
    )
