import numpy as np
import pandas as pd
from get_parameters import param_dict_extract

def admittance(parameter_dict):
    """Calculate the acoustic-to-electric and electric-to-acoustic transfer functions.

    Args:
        parameter_dict (_type_): _description_
        z_load_to_backing (_type_): _description_
        z_backing_to_load (_type_): _description_
    """
    # ==================================
    # Parameters
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
    
    # num_steps = int((f_max - f_min) / df) + 1
    # f = np.linspace(f_min, f_max, num_steps)
    
    # df = 0.0100 * 1e6
    # f_min = df
    # f_max = 20 * 1e6
    # f = np.arange(f_min, f_max + df, df)
    
    # len_f = len(f)
    # w = 2 * np.pi * f
    w = w.reshape(1, -1)  # transposing angular frequency vector
    
    unit_area = 1e-6  # unit area of 1mm in meters
    eps = 8.854e-12  # permittivity of free space
    c_0 = (eps * eps_r * unit_area) / d_piezo  # clamped capacitance
    #z_elport_termination = z_elport_termination * 50 # impedance of electrical port termination
    z_elport_termination = 0
    P = np.zeros((len_piezo, len_f))
    P = (h**2 * c_0) / (
        w * (1 + 1j * w * c_0 * z_elport_termination)
    )  # eq. 4.
    
    c_front_layers = c_front_layers.to_numpy().reshape(-1, 1)
    d_front_layers = d_front_layers.to_numpy().reshape(-1, 1)
    q_front_layers = q_front_layers.to_numpy().reshape(-1, 1)
    z_c_front_layers = z_c_front_layers.to_numpy().reshape(-1, 1)
    
    c_back_layers = c_back_layers.to_numpy().reshape(-1, 1)
    d_back_layers = d_back_layers.to_numpy().reshape(-1, 1)
    q_back_layers = q_back_layers.to_numpy().reshape(-1, 1)
    z_c_back_layers = z_c_back_layers.to_numpy().reshape(-1, 1)
    
    # a_11_front = np.zeros((len_front_layers, len_f), dtype=complex) # Initializing transfer function matrices prior to if-loop
    # a_12_front = np.zeros((len_front_layers, len_f), dtype=complex)
    # a_21_front = np.zeros((len_front_layers, len_f), dtype=complex)
    # a_22_front = np.zeros((len_front_layers, len_f), dtype=complex)
    
    # a_11_back = np.zeros((len_back_layers, len_f), dtype=complex)
    # a_12_back = np.zeros((len_back_layers, len_f), dtype=complex)
    # a_21_back = np.zeros((len_back_layers, len_f), dtype=complex)
    # a_22_back = np.zeros((len_back_layers, len_f), dtype=complex)
    
    #TODO TODO -- Should z_c_* be multiplied by unit_area?
    
    ### Front layers ###
    q_front_rec = 1 / q_front_layers
    z_c_front_layers = (1 + 0.5j * q_front_rec) * unit_area * z_c_front_layers
    #z_c_front_layers = (1 + 0.5j * q_front_rec) * z_c_front_layers
    kd_front = ((1 - 0.5j * q_front_rec) * d_front_layers / c_front_layers) * w

    a_11_front = np.cos(kd_front)
    a_12_front = -1j * z_c_front_layers * np.sin(kd_front)
    a_21_front = 1j * np.sin(kd_front) / z_c_front_layers
    a_22_front = -a_11_front
    
    # if len_front_layers != 0:
        
    #     q_front_rec = 1 / q_front_layers
    #     z_c_front_layers = (1 + 0.5j * q_front_rec) * unit_area * z_c_front_layers
    #     kd_front = ((1 - 0.5j * q_front_rec) * d_front_layers / c_front_layers) * w
    
    #     a_11_front = np.cos(kd_front)
    #     a_12_front = -1j * z_c_front_layers * np.sin(kd_front)
    #     a_21_front = 1j * np.sin(kd_front) / z_c_front_layers
    #     a_22_front = -a_11_front
    
    # else:
    #     q_front_rec = 0
    #     z_c_front_layers = 0
    #     kd_front = 0        
    #     a_11_front = np.zeros((0, len_f), dtype=complex) # Initializing transfer function matrices prior to if-loop
    #     a_12_front = np.zeros((0, len_f), dtype=complex)
    #     a_21_front = np.zeros((0, len_f), dtype=complex)
    #     a_22_front = np.zeros((0, len_f), dtype=complex)

    ### Back layers ###
    q_back_rec = 1 / q_back_layers
    z_c_back_layers = (1 + 0.5j * q_back_rec) * unit_area * z_c_back_layers
    #z_c_back_layers = (1 + 0.5j * q_back_rec) * z_c_back_layers
    kd_back = ((1 - 0.5j * q_back_rec) * d_back_layers / c_back_layers) * w
    
    a_11_back = np.cos(kd_back)
    a_12_back = -1j * z_c_back_layers * np.sin(kd_back)
    a_21_back = 1j * np.sin(kd_back) / z_c_back_layers
    a_22_back = -a_11_back
      
    # if len_back_layers != 0:
        
    #     q_back_rec = 1 / q_back_layers
    #     z_c_back_layers = (1 + 0.5j * q_back_rec) * unit_area * z_c_back_layers
    #     kd_back = ((1 - 0.5j * q_back_rec) * d_back_layers / c_back_layers) * w
        
    #     a_11_back = np.cos(kd_back)
    #     a_12_back = -1j * z_c_back_layers * np.sin(kd_back)
    #     a_21_back = 1j * np.sin(kd_back) / z_c_back_layers
    #     a_22_back = -a_11_back

    # else:
        
    #     a_11_back = np.zeros((1, len_f), dtype=complex) # Initializing transfer function matrices prior to if-loop
    #     a_12_back = np.zeros((1, len_f), dtype=complex)
    #     a_21_back = np.zeros((1, len_f), dtype=complex)
    #     a_22_back = np.zeros((1, len_f), dtype=complex)
    
    ### Other layers ###
    q_load_rec = 1 / q_load 
    q_piezo_rec = 1 / q_piezo
    q_backing_rec = 1 / q_backing
    
    z_c_load = (1 + 0.5j * q_load_rec) * unit_area * z_c_load
    #z_c_load = (1 + 0.5j * q_load_rec) * z_c_load
    z_c_piezo = (1 + 0.5j * q_piezo_rec) * unit_area * z_c_piezo
    #z_c_piezo = (1 + 0.5j * q_piezo_rec) * z_c_piezo
    z_c_backing = (1 + 0.5j * q_backing_rec) * unit_area * z_c_backing
    #z_c_backing = (1 + 0.5j * q_backing_rec) * z_c_backing
    
    kd_piezo = ((1 - 0.5j * q_piezo_rec) * d_piezo / c_piezo) * w
    
    a_11_piezo = (z_c_piezo * np.cos(kd_piezo) - P * np.sin(kd_piezo)) / (z_c_piezo - P * np.sin(kd_piezo))
    a_12_piezo = (
        -1j
        * z_c_piezo
        * (z_c_piezo * np.sin(kd_piezo) - 2 * P * (1 - np.cos(kd_piezo)))
        / (z_c_piezo - P * np.sin(kd_piezo))
    )
    a_21_piezo = (1j * np.sin(kd_piezo)) / (z_c_piezo - P * np.sin(kd_piezo))
    a_22_piezo = -a_11_piezo
    
    # ==================================
    # Mechanical Admittance (?)
    # ==================================
    
    ### Mechanical loading on piezo front face ###
    
    # Front layers
    if len_front_layers > 0:
        # Initialize z_front with the correct shape
        z_front = np.zeros((len_front_layers, len_f), dtype=complex)
        
        # For a single layer, directly calculate without looping
        if len_front_layers == 1:
            z_front[0, :] = (-(a_22_front[0, :] * z_c_load + a_12_front[0, :]) /
                            (a_21_front[0, :] * z_c_load + a_11_front[0, :]))
        else:
            # Calculate impedance for the layer closest to the load (last layer)
            z_front[-1, :] = (-(a_22_front[-1, :] * z_c_load + a_12_front[-1, :]) /
                            (a_21_front[-1, :] * z_c_load + a_11_front[-1, :]))

            # Iterate backwards from the second-last layer to the first
            for k in range(len_front_layers - 2, -1, -1):
                # Calculate the impedance for each layer using the impedance of the layer ahead
                z_front[k, :] = (-(a_22_front[k, :] * z_front[k+1, :] + a_12_front[k, :]) /
                                (a_21_front[k, :] * z_front[k+1, :] + a_11_front[k, :]))

    else:
        z_front = np.zeros((1, len_f), dtype=complex)
        z_front[0, :] = z_c_load
    
    # # Piezo layers
    # z_piezo = (-(a_22_piezo * z_front[0, :] + a_12_piezo) /
    #             (a_21_piezo * z_front[0, :] + a_11_piezo))
    
    ### Mechanical loading on piezo back face ###

    # Back layers
    z_back_reverse = np.zeros((len_back_layers, len_f), dtype=complex)

    if len_back_layers > 0:
    
        z_back_reverse = np.zeros((len_back_layers, len_f), dtype=complex)
        
        # For a single layer, directly calculate without looping
        if len_back_layers == 1:
            z_back_reverse[0, :] = (-(a_22_back[0, :] * z_c_backing + a_12_back[0, :]) /
                                    (a_21_back[0, :] * z_c_backing + a_11_back[0, :]))
        else:
            # Calculate impedance for the layer closest to the backing (last layer)
            z_back_reverse[-1, :] = (-(a_22_back[-1, :] * z_c_backing + a_12_back[-1, :]) /
                                     (a_21_back[-1, :] * z_c_backing + a_11_back[-1, :]))

            # Iterate backwards from the second-last layer to the first
            for k in range(len_back_layers - 2, -1, -1):
                # Calculate the impedance for each layer using the impedance of the layer ahead
                z_back_reverse[k, :] = (-(a_22_back[k, :] * z_back_reverse[k+1, :] + a_12_back[k, :]) /
                                        (a_21_back[k, :] * z_back_reverse[k+1, :] + a_11_back[k, :]))

    else:
        z_back_reverse = np.zeros((1, len_f), dtype=complex)
        z_back_reverse[0, :] = z_c_backing  # Assuming z_c_backing is the impedance to use when no layers are present
    
    # Piezo layers
    z_piezo_reverse = (-(a_22_piezo * z_back_reverse[0, :] + a_12_piezo) /
                        (a_21_piezo * z_back_reverse[0, :] + a_11_piezo))
    
    ### Front layers in reverse
    z_front_reverse = np.zeros((len_front_layers, len_f), dtype=complex)
    
    if len_front_layers > 0:
        z_front_reverse = np.zeros((len_front_layers, len_f), dtype=complex)
        
        # For a single layer, directly calculate without looping
        if len_front_layers == 1:
            z_front_reverse[0, :] = (-(a_22_front[0, :] * z_piezo_reverse + a_12_front[0, :]) /
                                     (a_21_front[0, :] * z_piezo_reverse + a_11_front[0, :]))
        else:
            # Calculate impedance for the layer closest to the piezo (first layer)
            z_front_reverse[0, :] = (-(a_22_front[0, :] * z_piezo_reverse + a_12_front[0, :]) /
                                     (a_21_front[0, :] * z_piezo_reverse + a_11_front[0, :]))

            # Iterate forward from the second layer to the last
            for k in range(1, len_front_layers):
                # Calculate the impedance for each layer using the impedance of the layer behind
                z_front_reverse[k, :] = (-(a_22_front[k, :] * z_front_reverse[k-1, :] + a_12_front[k, :]) /
                                         (a_21_front[k, :] * z_front_reverse[k-1, :] + a_11_front[k, :]))

    else: 
        pass
    
    # ==========================
    # Reflection Coefficient
    # ==========================
    
    # z_l  = z_backing_to_load[-1,:] # The total impedance seen from the backing (calculating from backing to layer interfacing with load)
    if len_front_layers > 0:
        z_l = z_front_reverse[0, :]
    else:
        z_l = z_piezo_reverse
        
    reflection_coefficient = (z_l - z_c_load) / (z_l + z_c_load) # Reflection coefficient at the front of layer interfacing with the load
    
    # ==========================
    # Force and Velocity Calculations
    # ==========================
    
    #TODO -- Add handling for 0 and 1 layer cases!
    
    # Front part of structure
    v_interfaces_front = np.zeros((len_front_layers + 1, len_f), dtype=complex)
    F_interfaces_front = np.zeros((len_front_layers + 1, len_f), dtype=complex)
    
    v_interfaces_front[-1, :] = 2 * unit_area / (z_c_load + z_l) # Initial Force/voltage. Layer interfacing with load (Index [-1]).
    F_interfaces_front[-1, :] = v_interfaces_front[-1, :] * z_l
    
    if len_front_layers != 0:
        for k in range(len_front_layers - 1, -1, -1): # Reamining layers. [-1] layer next to load. [0] layer next to piezo.
            v_interfaces_front[k, :] = -(a_21_front[k, :] * F_interfaces_front[k + 1, :] + 
                                         a_22_front[k, :] * v_interfaces_front[k + 1, :])
        
            F_interfaces_front[k, :] = (a_11_front[k, :] * F_interfaces_front[k + 1, :] + 
                                        a_12_front[k, :] * v_interfaces_front[k + 1, :])
    else:
        pass # This leaves the initial values as the only values in the arrays

    # Piezo layer
    v_interfaces_piezo = np.zeros((1, len_f), dtype=complex)
    F_interfaces_piezo = np.zeros((1, len_f), dtype=complex)

    v_interfaces_piezo[-1, :] = -(a_21_piezo[-1, :] * F_interfaces_front[0, :] + 
                                  a_22_piezo[-1, :] * v_interfaces_front[0, :])
    
    F_interfaces_piezo[-1, :] = (a_11_piezo[-1, :] * F_interfaces_front[0, :] + 
                                 a_12_piezo[-1, :] * v_interfaces_front[0, :])
    
    # Back part of structure
    if len_back_layers != 0:
        
        v_interfaces_back = np.zeros((len_back_layers + 1, len_f), dtype=complex)
        F_interfaces_back = np.zeros((len_back_layers + 1, len_f), dtype=complex)
        
        
        v_interfaces_back[0, :] = -(a_21_back[0, :] * F_interfaces_piezo[0, :] + 
                                    a_22_back[0, :] * v_interfaces_piezo[0, :])
        
        F_interfaces_back[0, :] = (a_11_back[0, :] * F_interfaces_piezo[0, :] + 
                                    a_12_back[0, :] * v_interfaces_piezo[0, :])
    
        for k in range(1, len_back_layers + 1):
            v_interfaces_back[k, :] = -(a_21_back[k - 1, :] * F_interfaces_back[k - 1, :] + 
                                        a_22_back[k - 1, :] * v_interfaces_back[k - 1, :])
            
            F_interfaces_back[k, :] = (a_11_back[k - 1, :] * F_interfaces_back[k - 1, :] + 
                                        a_12_back[k - 1, :] * v_interfaces_back[k - 1, :])
            
    else:
        pass
        

    # ==================================
    # Admittance Matrix
    # ==================================
    
    I_elport = ( # Current and voltage at the electrical port
        0.5
        * h
        * c_0
        * (v_interfaces_front[0, :] - v_interfaces_piezo)
        / (1 + 1j * w * c_0 * z_elport_termination)
    )
    V_elport = -I_elport * z_elport_termination
    
    y_sys = np.zeros((len_piezo + 1, len_piezo + 1, len_f), dtype=complex)
    
    y_sys[0:len_piezo, len_piezo-1, :] = np.reshape(
        I_elport, (len_piezo, 1, len_f)
    )  # TODO: Is this correct y_sys array position (upper left)?
    y_sys[len_piezo, len_piezo, :] = (
        0.5 * v_interfaces_front[-1, :]
    )  # TODO: Is this correct y_sys array position (lower right)?

    y_1 = 1 / (1j * z_c_piezo * np.tan(0.5 * kd_piezo))
    y_2 = y_1
    y_3 = 1 / (-1j * z_c_piezo / np.sin(kd_piezo) + 1j * (h**2 * c_0) * (1 / w))

    phi = h * c_0
    y_11 = y_1 * (y_2 + y_3) / (y_1 + y_2 + y_3)
    y_12 = -y_1 * y_2 / (y_1 + y_2 + y_3)
    y_13 = -phi * y_1 * y_3 / (y_1 + y_2 + y_3)
    y_22 = y_11
    y_21 = y_12
    y_31 = y_13
    y_23 = y_13
    y_32 = y_13
    y_33 = 1j*c_0*w + phi**2 * y_3 * (y_1 + y_2) / (y_1 + y_2 + y_3)

    z_front_total = z_front[0, :] # Mechanical loading on front face of piezo
    z_back_total = z_back_reverse[0, :] # Mechanical loading on back face of piezo

    determinant = (1 + y_11 * z_back_total) * (1 + y_22 * z_front_total) - y_21 * z_back_total * y_12 * z_front_total
    v_piezo_front = -(y_13 * (1 + y_22 * z_front_total) - y_23 * y_12 * z_front_total) / determinant # Velocity at front face of piezo | # VI2(k)
    F_piezo_front = v_piezo_front * z_front_total # Force at front face of piezo | # VI1(k)
    v_piezo_back = (-y_13 * y_21 * z_back_total + y_23 * (1 + y_11 * z_back_total)) / determinant  # VI2(k+1)
    F_piezo_back = -v_piezo_back * z_front_total # VI1(k+1)

    Y_el = y_31 * F_piezo_front + y_32 * F_piezo_back + y_33 # electrical admittance
    
    # H_tt (calculated with unit voltage (V3 = 1V) )
    
    ##### F_htt = VI1(lenp+1, :) = F_piezo_back
    ##### v_htt = VI2(lenp+1, :) = v_piezo_back
    
    # F_htt = np.zeros((1, len_f), dtype=complex)
    # v_htt = np.zeros((1, len_f), dtype=complex)
    
    # F_htt[0,:] = F_piezo_back
    # v_htt[0,:] = v_piezo_back
    
    # for k in range(0, len_front_layers):
    #     v_htt[k+1, :] = a_11_front[k, :] * v_htt[k, :] - a_12_front[k, :] * F_htt[k, :]
    #     F_htt[k+1, :] = a_21_front[k, :] * v_htt[k, :] - a_22_front[k, :] * F_htt[k, :]
    
    # h_tt = -v_htt[-1, :]
    
    
    
    # %TFJ: for den 3-porten beregne, vha. admittansematrisen over, Strømmer og spenninger dersom en setter V3=1 (Volt)
    # Detr = (1+Y11.*ZIk).*(1+Y22.*ZLp1)-Y21.*ZIk.*Y12.*ZLp1;
    # VI2(k,:)=-(Y13.*(1+Y22.*ZLp1) - Y23.*Y12.*ZLp1)./Detr; 
    # VI2(k+1,:)=(-Y13.*Y21.*ZIk + Y23.*(1+Y11.*ZIk))./Detr; 
    # VI1(k,:)=VI2(k,:).*ZIk;
    # VI1(k+1,:)=-VI2(k+1,:).*ZLp1;
    
    # %TFJ: Her beregnes hastigheten på overflaten av transduseren ved V3=1 (Volt), dvs. H_tt | %bør nulle ut VI1m, og VI2m
    # VI1m(1,:)=VI1(lenp+1,:);
    # VI2m(1,:)=VI2(lenp+1,:);  
    # for K=1:lenm
    #     VI1m(K+1,:)=a11m(K,:).*VI1m(K,:) - a12m(K,:).*VI2m(K,:);
    #     VI2m(K+1,:)=a21m(K,:).*VI1m(K,:) - a22m(K,:).*VI2m(K,:);
    # end

    # %Y_sys(lenp+1,k,:) = VI2m(K+1,:);
    # Y_sys(aSizeYm1+1,vPntPiezo(k),:) = -VI2m(K+1,:);
    
    h_tt = 1
    
    return Y_el, h_tt, f, unit_area
    
        
# ==================================
# ==================================
if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator
    from get_parameters import get_parameters
    from mechanical_impedance import mechanical_impedance
    from transfer_functions import admittance

    # Get variables
    #struct_filename = "struct_0front_0back_air_air.xlsx"
    #struct_filename = "struct_0front_1back_water_air.xlsx"
    struct_filename = "struct_0front_3back_water_air.xlsx"

    
    materials_data, parameter_dict = get_parameters(struct_filename)
    
    # Mechanical Impedance
    (
        z_load_to_backing,
        z_backing_to_load,
        z_in_front,
        z_in_piezo,
        z_in_back,
        z_in_back_reverse,
        z_in_piezo_reverse,
        z_in_front_reverse,
    ) = mechanical_impedance(parameter_dict)
    
    Y_el, h_tt, f, unit_area = admittance(parameter_dict)
    
    # ==================================
    # Plotting electrical impedance
    # ==================================
    f = parameter_dict["f"]
    f = f.reshape(1, -1) / 1e6
    
    # df = 0.01e6
    # f_min = df
    # f_max = 20e6
    # f = np.arange(df, f_max + df, df) / 1e6
    #f = f / 1e6
    
    Z_el = 1 / Y_el
    #Z_el = Z_el / unit_area
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    # Plotting absolute value
    ax1.plot(f.flatten(), np.abs(Z_el.flatten()))
    ax1.set_ylabel('|Z_el|')
    ax1.set_title('Electrical Admittance')
    ax1.set_ylim(0, 10000)
    ax1.grid(True)

    # Plotting phase in degrees
    ax2.plot(f.flatten(), np.angle(Z_el.flatten(), deg=True))
    ax2.set_xlabel('Frequency (MHz)')
    ax2.set_ylabel('Phase (degrees)')

    # Set x-axis tick labels for each 1MHz and every 0.5MHz
    ax2.set_xticks(np.arange(min(f.flatten()), max(f.flatten())+1, 0.5), minor=True)
    ax2.set_xticks(np.arange(min(f.flatten()), max(f.flatten())+1, 1))
    ax2.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax2.xaxis.set_tick_params(which='minor', labelbottom=False)

    # Enable grid for both major and minor ticks
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax2.grid(which='both', linestyle='--', linewidth=0.5)

    plt.show()
    
    # ==================================
    # Plotting transfer functions
    # =================================
    
    # fig, ax = plt.subplots()
    # ax.plot(f.flatten(), np.abs(h_tt.flatten()))
    # ax.set_xlabel('Frequency (MHz)')
    # ax.set_ylabel('|h_tt|')
    # ax.set_title('Absolute Value of h_tt')
    # ax.grid(True)
    # plt.show()