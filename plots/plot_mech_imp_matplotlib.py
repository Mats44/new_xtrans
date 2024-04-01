import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mplcursors
import numpy as np
from get_parameters import param_dict_extract

def plot_mech_imp_fwd(z_in_front, z_in_piezo, z_in_back, z_c_backing, f, f_min, f_max):
    """
    Plot the mechanical impedance seen towards the backing (load -> piezo -> backing)
    using Matplotlib.
    """
    f = f / 1e6  # convert to MHz
    f_min = f_min / 1e6
    f_max = f_max / 1e6

    line_width = 1
    
    size = 10
    cmap = plt.cm.get_cmap('viridis', size) # Generate a color map
    colors = [cmap(i) for i in range(size)] # Generate colors from the color map

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Mech Z Forward (load->backing)', fontsize=14)

    # # Plot z_c_backing
    # z_c_backing = z_c_backing / 1e6
    # line_color_piezo = 'gold'  # Single color for all z_in_piezo lines
    # for i, row in enumerate(z_in_piezo):
    #     axs[0, 0].plot(f, np.real(row), color=line_color_piezo, linewidth=line_width, label=f'Piezo layer')
    #     axs[0, 1].plot(f, np.abs(row), color=line_color_piezo, linewidth=line_width)
    #     axs[1, 0].plot(f, np.imag(row), color=line_color_piezo, linewidth=line_width)
    #     axs[1, 1].plot(f, np.angle(row, deg=True), color=line_color_piezo, linewidth=line_width)

    # Plot z_in_front
    z_in_front = z_in_front / 1e6 # Convert to MRayl
    colors = ['blue', 'green', 'red', 'purple']
    
    for i, row in enumerate(z_in_front):
        color = colors[i]

        axs[0, 0].plot(f, np.real(row), color=color, linewidth=line_width, label=f'Front layer {i+1}')
        axs[0, 1].plot(f, np.abs(row), color=color, linewidth=line_width, label=f'Front layer {i+1}')
        axs[1, 0].plot(f, np.imag(row), color=color, linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color=color, linewidth=line_width)

    # Plot z_in_piezo
    z_in_piezo = z_in_piezo / 1e6
    for i, row in enumerate(z_in_piezo):
        axs[0, 0].plot(f, np.real(row), color='gold', linewidth=line_width, label=f'Piezo layer')
        axs[0, 1].plot(f, np.abs(row), color='gold', linewidth=line_width, label=f'Piezo layer')
        axs[1, 0].plot(f, np.imag(row), color='gold', linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color='gold', linewidth=line_width)

    # Plot z_in_back
    z_in_back = z_in_back / 1e6
    colors= ['orange', 'cyan', 'magenta', 'teal']
    
    for i, row in enumerate(z_in_back):
        color = colors[i]

        axs[0, 0].plot(f, np.real(row), color=color, linewidth=line_width, label=f'Back layer {i+1}')
        axs[0, 1].plot(f, np.abs(row), color=color, linewidth=line_width, label=f'Back layer {i+1}')
        axs[1, 0].plot(f, np.imag(row), color=color, linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color=color, linewidth=line_width)
        
    # Set the x-axis limits and titles
    for ax in axs.flat:
        ax.set_xlim([f_min, f_max])
        ax.set_xlabel('Frequency [MHz]')

    # Set the y-axis titles
    axs[0, 0].set_ylabel('Re{z_fwd} [MRayl]')
    axs[0, 1].set_ylabel('|z_fwd| [MRayl]')
    axs[1, 0].set_ylabel('Im{z_fwd} [MRayl]')
    axs[1, 1].set_ylabel(' z_fwd Phase [deg]')

    # Show legends
    axs[0, 1].legend(loc='upper right')

    # Show the plot
    plt.tight_layout()
    

def plot_mech_imp_bwd(z_in_front_reverse, z_in_piezo_reverse, z_in_back_reverse, f, f_min, f_max):
    """
    Plot the mechanical impedance seen towards the load (backing -> piezo -> load)
    using Matplotlib.
    """
    f = f / 1e6  # convert to MHz
    f_min = f_min / 1e6
    f_max = f_max / 1e6

    line_width = 1
    
    size = 10
    cmap = plt.cm.get_cmap('viridis', size) # Generate a color map
    colors = [cmap(i) for i in range(size)] # Generate colors from the color map

    # Create a figure with subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Mech Z Backward (backing->load)', fontsize=14)

    # Plot z_in_back_reverse
    z_in_back_reverse = z_in_back_reverse / 1e6
    colors = ['blue', 'green', 'red', 'purple']
    
    for i, row in enumerate(z_in_back_reverse):
        color = colors[i]

        axs[0, 0].plot(f, np.real(row), color=color, linewidth=line_width, label=f'Back layer {i+1}')
        axs[0, 1].plot(f, np.abs(row), color=color, linewidth=line_width, label=f'Back layer {i+1}')
        axs[1, 0].plot(f, np.imag(row), color=color, linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color=color, linewidth=line_width)

    # Plot z_in_piezo_reverse
    z_in_piezo_reverse = z_in_piezo_reverse / 1e6
    for i, row in enumerate(z_in_piezo_reverse):
        axs[0, 0].plot(f, np.real(row), color='gold', linewidth=line_width, label=f'Piezo layer')
        axs[0, 1].plot(f, np.abs(row), color='gold', linewidth=line_width, label=f'Piezo layer')
        axs[1, 0].plot(f, np.imag(row), color='gold', linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color='gold', linewidth=line_width)

    # Plot z_in_front_reverse
    z_in_front_reverse = z_in_front_reverse / 1e6 # Convert to MRayl
    colors= ['orange', 'cyan', 'magenta', 'teal']
    
    for i, row in enumerate(z_in_front_reverse):
        #color = color_scale(i / len(z_in_front_reverse))
        color = colors[i]

        axs[0, 0].plot(f, np.real(row), color=color, linewidth=line_width, label=f'Front layer {i+1}')
        axs[0, 1].plot(f, np.abs(row), color=color, linewidth=line_width, label=f'Front layer {i+1}')
        axs[1, 0].plot(f, np.imag(row), color=color, linewidth=line_width)
        axs[1, 1].plot(f, np.angle(row, deg=True), color=color, linewidth=line_width)

    # Set the x-axis limits and titles
    for ax in axs.flat:
        ax.set_xlim([f_min, f_max])
        ax.set_xlabel('Frequency [MHz]')

    # Set the y-axis titles
    axs[0, 0].set_ylabel('Re{z_bwd} [MRayl]')
    axs[0, 1].set_ylabel('|z_bwd| [MRayl]')
    axs[1, 0].set_ylabel('Im{z_bwd} [MRayl]')
    axs[1, 1].set_ylabel('z_bwd Phase [deg]')

    # Show legends
    axs[0, 1].legend(loc='upper right')

    # Show the plot
    plt.tight_layout()

    
    
def plot_mech_imp_matplotlib(z_load_to_backing, z_backing_to_load, z_in_front, z_in_piezo,
                             z_in_back, z_in_back_reverse, z_in_piezo_reverse, z_in_front_reverse, parameter_dict):
    
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



    plot_mech_imp_fwd(z_in_front, z_in_piezo, z_in_back, z_c_backing, f, f_min, f_max)
    plot_mech_imp_bwd(z_in_front_reverse, z_in_piezo_reverse, z_in_back_reverse, f, f_min, f_max)
    
    plt.show()