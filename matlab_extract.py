import scipy.io
import numpy as np
import matplotlib.pyplot as plt

def extract_sXtransParam_fields(mat_file_path):
    # Load the MATLAB file
    mat_data = scipy.io.loadmat(mat_file_path)
    
    # Access the 'sXtransParam' struct. It's assumed to be at the top level.
    sXtransParam_struct = mat_data['sXtransParam'][0, 0]
    
    sXtransParam_fields = {}

    # List of field names
    field_names = [
        'NR_Piezolay', 'NR_Matchlay', 'FREQ', 'FREQ1', 'EXFR', 'FMIN', 'FMAX', 'AR', 'AR1',
        'NHC', 'df', 'zb', 'cb', 'qb', 'useF1', 'useAR1', 'z', 'c', 'q', 'h', 'epsr', 'l',
        'Zel', 'betan', 'zm', 'cm', 'qm', 'lm', 'betanm', 'zl', 'cl', 'ql', 'Y_sys'
    ]

    # Extract each field and store in the dictionary
    for field in field_names:
        sXtransParam_fields[field] = sXtransParam_struct[field][0, 0]

    return sXtransParam_fields


def extract_xtrans_mech_imp(load_to_backing_path, backing_to_load_path):
    load_to_backing = scipy.io.loadmat(load_to_backing_path)
    backing_to_load = scipy.io.loadmat(backing_to_load_path)

    xtrans_z_load_to_backing = load_to_backing['Z_fwd']
    xtrans_z_backing_to_load = backing_to_load['Z_fwd']

    xtrans_z_load_to_backing = xtrans_z_load_to_backing.T
    xtrans_z_backing_to_load = xtrans_z_backing_to_load.T
    
    return xtrans_z_load_to_backing, xtrans_z_backing_to_load

def extract_electrical_imp(z_el_path):
    xtrans_z_el = scipy.io.loadmat(z_el_path)
    
    xtrans_z_el = xtrans_z_el['Z_i']
    xtrans_z_el = xtrans_z_el.T
    
    return xtrans_z_el
    
def plot_electrical_impedance(xtrans_z_el, Y_el, f_el):
    
    f_el = f_el / 1e6
    Z_el = 1 / Y_el
    Z_el = Z_el.flatten()
    xtrans_z_el = xtrans_z_el.flatten()

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Plot absolute value in the first subplot
    ax1.plot(f_el, np.abs(Z_el), linestyle='-', label='Z_el')
    ax1.plot(f_el, np.abs(xtrans_z_el), linestyle='--', label='xtrans_z_el')
    ax1.set_xlabel('Frequency (MHz)')
    ax1.set_ylabel('|Z_i| [Ohms]')
    ax1.set_ylim(0, 10000)
    ax1.legend()

    # Plot phase in the second subplot
    ax2.plot(f_el, np.angle(Z_el, deg=True), linestyle='-', label='Z_el')
    ax2.plot(f_el, np.angle(xtrans_z_el, deg=True), linestyle='--', label='xtrans_z_el')
    ax2.set_xlabel('Frequency (MHz)')
    ax2.set_ylabel('Phase (degrees)')
    ax2.legend()

    plt.tight_layout()
    plt.show()


def plot_mechanical_impedance(xtrans_z_load_to_backing, xtrans_z_backing_to_load, z_load_to_backing, z_backing_to_load, f):
    # Z_LOAD_TO_BACKING
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle('Mechanical Impedance: Load to Backing')

    # Real part
    for row in xtrans_z_load_to_backing:
        ax1.plot(f, np.real(row))
    ax1.set_ylabel('Real Part [MRayls]')

    # Absolute value
    for row in xtrans_z_load_to_backing:
        ax2.plot(f, np.abs(row))

    ax2.set_ylabel('Absolute Value [MRayls]')

    # Imaginary part
    for row in xtrans_z_load_to_backing:
        ax3.plot(f, np.imag(row))

    ax3.set_xlabel('Frequency (MHz)')
    ax3.set_ylabel('Imaginary Part [MRayls]')

    # Phase in degrees
    for row in xtrans_z_load_to_backing:
        ax4.plot(f, np.angle(row, deg=True))

    ax4.set_xlabel('Frequency (MHz)')
    ax4.set_ylabel('Phase (degrees)')

    ax2.legend(['Row 1', 'Row 2', 'Row 3', ...])

    # Z_BACKING_TO_LOAD
    fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
    fig2.suptitle('Mechanical Impedance: Backing to Load')

    # Real part
    for row in xtrans_z_backing_to_load:
        ax1.plot(f, np.real(row))
    ax1.set_ylabel('Real Part')

    # Absolute value
    for row in xtrans_z_backing_to_load:
        ax2.plot(f, np.abs(row))

    ax2.set_ylabel('Absolute Value')

    # Imaginary part
    for row in xtrans_z_backing_to_load:
        ax3.plot(f, np.imag(row))

    ax3.set_xlabel('Frequency (MHz)')
    ax3.set_ylabel('Imaginary Part')

    # Phase in degrees
    for row in xtrans_z_backing_to_load:
        ax4.plot(f, np.angle(row, deg=True))

    ax4.set_xlabel('Frequency (MHz)')
    ax4.set_ylabel('Phase (degrees)')

    ax2.legend(['Row 1', 'Row 2', 'Row 3', ...])

    plt.tight_layout()
    plt.show()


def plot_mechanical_impedance_combined(xtrans_z_load_to_backing, xtrans_z_backing_to_load, z_load_to_backing, z_backing_to_load, f):
    
    xtrans_z_load_to_backing = xtrans_z_load_to_backing / 1e6
    xtrans_z_backing_to_load = xtrans_z_backing_to_load / 1e6
    z_load_to_backing = z_load_to_backing / 1e6
    z_backing_to_load = z_backing_to_load / 1e6
    f = f / 1e6
    
    # Z_LOAD_TO_BACKING
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle('Mechanical Impedance: Load to Backing')

    # Real part
    for row in xtrans_z_load_to_backing:
        ax1.plot(f, np.real(row), linestyle='--')
    for row in z_load_to_backing:
        ax1.plot(f, np.real(row), linestyle='-', alpha=0.5)
    ax1.set_ylabel('Real Part [MRayls]')

    # Absolute value
    for row in xtrans_z_load_to_backing:
        ax2.plot(f, np.abs(row), linestyle='--')
    for row in z_load_to_backing:
        ax2.plot(f, np.abs(row), linestyle='-', alpha=0.5)
    ax2.set_ylabel('Absolute Value [MRayls]')

    # Imaginary part
    for row in xtrans_z_load_to_backing:
        ax3.plot(f, np.imag(row), linestyle='--')
    for row in z_load_to_backing:
        ax3.plot(f, np.imag(row), linestyle='-', alpha=0.5)
    ax3.set_xlabel('Frequency (MHz)')
    ax3.set_ylabel('Imaginary Part [MRayls]')

    # Phase in degrees
    for row in xtrans_z_load_to_backing:
        ax4.plot(f, np.angle(row, deg=True), linestyle='--')
    for row in z_load_to_backing:
        ax4.plot(f, np.angle(row, deg=True), linestyle='-', alpha=0.5)
    ax4.set_xlabel('Frequency (MHz)')
    ax4.set_ylabel('Phase (degrees)')

    ax2.legend(['Row 1', 'Row 2', 'Row 3', 'z_load_to_backing'])

    # Z_BACKING_TO_LOAD
    fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
    fig2.suptitle('Mechanical Impedance: Backing to Load')

    # Real part
    for row in xtrans_z_backing_to_load:
        ax1.plot(f, np.real(row), linestyle='--')
    for row in z_backing_to_load:
        ax1.plot(f, np.real(row), linestyle='-', alpha=0.5)
    ax1.set_ylabel('Real Part [MRayls]')

    # Absolute value
    for row in xtrans_z_backing_to_load:
        ax2.plot(f, np.abs(row), linestyle='--')
    for row in z_backing_to_load:
        ax2.plot(f, np.abs(row), linestyle='-', alpha=0.5)
    ax2.set_ylabel('Absolute Value [MRayls]')

    # Imaginary part
    for row in xtrans_z_backing_to_load:
        ax3.plot(f, np.imag(row), linestyle='--')
    for row in z_backing_to_load:
        ax3.plot(f, np.imag(row), linestyle='-', alpha=0.5)
    ax3.set_xlabel('Frequency (MHz)')
    ax3.set_ylabel('Imaginary Part [MRayls]')

    # Phase in degrees
    for row in xtrans_z_backing_to_load:
        ax4.plot(f, np.angle(row, deg=True), linestyle='--')
    for row in z_backing_to_load:
        ax4.plot(f, np.angle(row, deg=True), linestyle='-', alpha=0.5)
    ax4.set_xlabel('Frequency (MHz)')
    ax4.set_ylabel('Phase (degrees)')

    ax2.legend(['Row 1', 'Row 2', 'Row 3', 'z_backing_to_load'])

    plt.tight_layout()
    plt.show()

###########################################
###########################################

if __name__ == "__main__":

    from mechanical_impedance import mechanical_impedance as mechanical_impedance
    from mechanical_impedance_loss import mechanical_impedance as mechanical_impedance_loss
    from get_parameters import get_parameters
    from transfer_functions import admittance

    ### MATLAB structures ###
    xtrans_param_path = 'parameters/matlab/xtrans_0front_0back_air_air.mat'

    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_0front_0back_air_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_0front_0back_air_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_1front_0back_air_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_1front_0back_air_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_1front_0back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_1front_0back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_1front_1back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_1front_1back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_1front_2back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_1front_2back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_2front_0back_air_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_2front_0back_air_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_2front_0back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_2front_0back_water_air.mat'
    
    load_to_backing_path = 'parameters/matlab/z_LoadToBacking_2front_1back_water_air.mat'
    backing_to_load_path = 'parameters/matlab/z_backingToLoad_2front_1back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_3front_0back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_3front_0back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_3front_1back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_3front_1back_water_air.mat'
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_3front_3back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_3front_3back_water_air.mat'
    
    
    
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_0front_1back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_0front_1back_water_air.mat'
    #load_to_backing_path = 'parameters/matlab/z_LoadToBacking_0front_3back_water_air.mat'
    #backing_to_load_path = 'parameters/matlab/z_backingToLoad_0front_3back_water_air.mat'
    


    #z_el_path = 'parameters/matlab/Zel_0front_0back_air_air.mat'
    #z_el_path = 'parameters/matlab/Zel_1front_0back_air_air.mat'
    #z_el_path = 'parameters/matlab/Zel_1front_0back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_1front_1back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_1front_2back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_2front_0back_air_air.mat'
    #z_el_path = 'parameters/matlab/Zel_2front_0back_water_air.mat'
    z_el_path = 'parameters/matlab/Zel_2front_1back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_3front_0back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_3front_1back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_3front_3back_water_air.mat'
    
    #z_el_path = 'parameters/matlab/Zel_0front_3back_water_air.mat'
    #z_el_path = 'parameters/matlab/Zel_0front_1back_water_air.mat'


    ### Python structures ###
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


    ### Extract sXtransParams data ###
    fields = extract_sXtransParam_fields(xtrans_param_path)

    # for field_name, value in fields.items():
    #     if field_name != 'Y_sys':
    #         print(f"{field_name}: {value}")

    ### Extract the MATLAB mechanical impedance data ###
    xtrans_z_load_to_backing, xtrans_z_backing_to_load = extract_xtrans_mech_imp(load_to_backing_path, backing_to_load_path)

    ### Extract the MATLAB electrical impedance data ###
    xtrans_z_el = extract_electrical_imp(z_el_path)

    ### Get Python mechanical impedance data ###
    materials_data, parameter_dict = get_parameters(struct_filename)
    
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

    ### Get Python electrical impedance data ###
    Y_el, H_tt, f_el, unit_area = admittance(parameter_dict)

    ### Plotting ###
    f = parameter_dict['f']

    #plot_mechanical_impedance(xtrans_z_load_to_backing, xtrans_z_backing_to_load, z_load_to_backing, z_backing_to_load, f) #only plots xtrans variables right now
    #plot_mechanical_impedance_combined(xtrans_z_load_to_backing, xtrans_z_backing_to_load, z_load_to_backing, z_backing_to_load, f)
    plot_electrical_impedance(xtrans_z_el, Y_el, f_el)
