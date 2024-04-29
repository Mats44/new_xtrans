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
    ax1.set_title('Electrical Impedance')
    ax1.set_ylim(0, 10000)
    ax1.grid(True)

    # Plotting phase in degrees
    ax2.plot(f.flatten(), np.angle(Z_el.flatten(), deg=True))
    ax2.set_xlabel('Frequency (MHz)')
    ax2.set_ylabel('Phase (degrees)')

    # Determine x-axis tick positions
    f_min, f_max = f.min(), f.max()
    x_ticks = np.arange(np.ceil(f_min), np.ceil(f_max) + 1, 1)  # Create ticks every 1 MHz, rounded up to the nearest MHz
    
    # Apply the tick positions and labels to both subplots
    for ax in [ax1, ax2]:
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([f"{x:.0f}" for x in x_ticks])  # Format as integer MHz
        ax.grid(which='both', linestyle='--', linewidth=0.5)
        #ax.minorticks_on()  # Enable minor ticks for more detailed grid control
    ax2.set_ylim(-90, 90)
    ax2.set_yticks(range(-90, 91, 30))

    # Enable grid for both major and minor ticks
    ax1.grid(which='both', linestyle='--', linewidth=0.5)
    ax2.grid(which='both', linestyle='--', linewidth=0.5)

    plt.show()