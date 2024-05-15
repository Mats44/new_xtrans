import math
# %% 
# ==================================
# Quarter-wavelength Thickness
# ==================================

fc = 3 * 1e6  # frequency in Hz
c = [4500, 3000, 3000]  # list of speeds

for item in c:
    d = (1/4 * item / fc) * 1e3  # quarter-wave thickness
    print(f"Quarter-wave thickness for speed {item}: {d} mm")

# %%      
# ==================================
# Desilet Impedances
# ==================================

# Constants
z_air = 0.000415 * 1e6  # Impedance of air in Rayls
z_water = 1.48 * 1e6  # Impedance of water in Rayls

Z_piezo = 34 * 1e6  # Impedance of the transducer material in Rayls
Z_load = z_air # Impedance of the load in Rayls
N = 2  # Number of layers

impedances = []

if N == 1:
    N1 = (Z_piezo ** (1 / 3) * Z_load ** (2 / 3)) / 1e6
    impedances.append(N1)
elif N == 2:
    N1 = (Z_piezo ** (4 / 7) * Z_load ** (3 / 7)) / 1e6
    N2 = (Z_piezo ** (1 / 7) * Z_load ** (6 / 7)) / 1e6
    impedances.append(N1)
    impedances.append(N2)
elif N == 3:
    N1 = (Z_piezo ** (11 / 15) * Z_load ** (4 / 15)) / 1e6
    N2 = (Z_piezo ** (5 / 15) * Z_load ** (10 / 15)) / 1e6
    N3 = (Z_piezo ** (1 / 15) * Z_load ** (14 / 15)) / 1e6
    impedances.append(N1)
    impedances.append(N2)
    impedances.append(N3)

# Print the calculated impedances in standard notation
for i, impedance in enumerate(impedances, start=1):
    print(f"Layer {i} Impedance: {format(impedance, '.6f')} MRayls")

# zp = 34*1e6
# zl = 0.000415*1e6
# test = (zp**(1/3) * zl**(2/3)) /1e6
# print(test)
# %%
