import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from get_parameters import param_dict_extract

def plot_transfer_functions(h_tt, coupling, f, parameter_dict):
    
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

    f = f / 1e6
    #h_tt = h_tt / 1e6

    # Plot absolute value of H_tt
    plt.subplot(2, 1, 1)
    plt.semilogy(f, np.abs(h_tt))
    plt.ylabel('|H_tt|')
    plt.title('Transfer Function')

    # Plot phase of H_tt
    plt.subplot(2, 1, 2)
    plt.plot(f, np.angle(h_tt, deg=True))
    plt.xlabel('Frequency [MHz]')
    plt.ylabel('Phase (degrees)')
    
    ax = plt.gca() # Define ax variable
    ax.set_ylim(-90, 90)
    ax.set_yticks(range(-90, 91, 30))

    # Add major and minor x-axis grid lines for the first subplot
    ax = plt.subplot(2, 1, 1)
    ax.xaxis.grid(True, which='both', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(True, which='minor', linestyle=':', linewidth=0.5)
    ax.xaxis.grid(True, which='major', linestyle='-', linewidth=0.5)
    ax.yaxis.grid(True, which='both', linestyle='-', linewidth=0.5)
    ax.yaxis.grid(True, which='minor', linestyle=':', linewidth=0.5)
    ax.yaxis.grid(True, which='major', linestyle='-', linewidth=0.5)

    # Add major and minor x-axis grid lines for the second subplot
    ax = plt.subplot(2, 1, 2)
    ax.xaxis.grid(True, which='both', linestyle='-', linewidth=0.5)
    ax.xaxis.grid(True, which='minor', linestyle=':', linewidth=0.5)
    ax.xaxis.grid(True, which='major', linestyle='-', linewidth=0.5)
    ax.yaxis.grid(True, which='both', linestyle='-', linewidth=0.5)
    ax.yaxis.grid(True, which='minor', linestyle=':', linewidth=0.5)
    ax.yaxis.grid(True, which='major', linestyle='-', linewidth=0.5)

    plt.tight_layout()

    # Show the plot
    plt.show()
    
