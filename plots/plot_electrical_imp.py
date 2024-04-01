import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mplcursors
import numpy as np
from get_parameters import param_dict_extract

def plot_electrical_imp(Y_el, f):
    
    f = f / 1e6
    Z_el = 1 / Y_el
    Z_el = Z_el.flatten()

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Plot absolute value in the first subplot
    ax1.plot(f, np.abs(Z_el), linestyle='-', label='Z_el')
    ax1.set_xlabel('Frequency (MHz)')
    ax1.set_ylabel('|Z_i| [Ohms]')
    ax1.legend()

    # Plot phase in the second subplot
    ax2.plot(f, np.angle(Z_el, deg=True), linestyle='-', label='Z_el')
    ax2.set_xlabel('Frequency (MHz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.legend()

    plt.tight_layout()
    plt.show()