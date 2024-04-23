import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

def plot_electrical_imp(Y_el, f):
    
    f = f.reshape(1, -1) / 1e6
    Z_el = 1 / Y_el
    
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