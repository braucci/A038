import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Constants
T0 = 288.15  # Sea level standard temperature (K)
P0 = 101325  # Sea level standard pressure (Pa)
rho0 = 1.225  # Sea level standard density (kg/m³)
R = 8.3144598  # Universal gas constant (J/(mol·K))
g = 9.80665  # Gravitational acceleration (m/s²)
M = 0.0289644  # Molar mass of Earth's air (kg/mol)

# Altitude range (0 to 86,000 meters)
h = np.linspace(0, 86000, 500)

# Temperature profile as a function of altitude
def temperature(h):
    if h <= 11000:
        return T0 + -0.0065 * h
    elif h <= 20000:
        return 216.65
    elif h <= 32000:
        return 216.65 + 0.001 * (h - 20000)
    elif h <= 47000:
        return 228.65 + 0.0028 * (h - 32000)
    elif h <= 51000:
        return 270.65
    elif h <= 71000:
        return 270.65 - 0.0028 * (h - 51000)
    else:
        return 214.65 - 0.002 * (h - 71000)

# Calculate temperature array
T = np.array([temperature(alt) for alt in h])

# Updated pressure profile function
def pressure(h):
    if h <= 11000:
        return P0 * (1 + (-0.0065 * h) / T0) ** (-g * M / (R * -0.0065))
    elif h <= 20000:
        return pressure(11000) * np.exp(-g * M * (h - 11000) / (R * 216.65))
    elif h <= 32000:
        return pressure(20000) * (1 + (0.001 * (h - 20000) / 216.65)) ** (-g * M / (R * 0.001))
    elif h <= 47000:
        return pressure(32000) * (1 + (0.0028 * (h - 32000) / 228.65)) ** (-g * M / (R * 0.0028))
    elif h <= 51000:
        return pressure(47000) * np.exp(-g * M * (h - 47000) / (R * 270.65))
    elif h <= 71000:
        return pressure(51000) * (1 - (0.0028 * (h - 51000) / 270.65)) ** (-g * M / (R * -0.0028))
    else:
        return pressure(71000) * (1 - (0.002 * (h - 71000) / 214.65)) ** (-g * M / (R * -0.002))

# Calculate pressure array
P = np.array([pressure(alt) for alt in h])

# Density as a function of altitude
rho = P * M / (R * T)

# Create a DataFrame to hold the results
isa_results = pd.DataFrame({
    'Altitude (m)': h,
    'Temperature (K)': T,
    'Pressure (Pa)': P,
    'Density (kg/m³)': rho
})

# Plotting the results
fig, axs = plt.subplots(1, 3, figsize=(18, 10), sharey=True)

# Temperature plot
axs[0].plot(T, h / 1000, color='tab:blue')
axs[0].set_xlabel('T(h) [K]')
axs[0].set_ylabel('Altitude [km]')
axs[0].grid(True)

# Pressure plot
axs[1].plot(P, h / 1000, color='tab:orange')
axs[1].set_xlabel('P(h) [Pa]')
axs[1].grid(True)

# Density plot
axs[2].plot(rho, h / 1000, color='tab:green')
axs[2].set_xlabel('ρ(h) [kg/m³]')
axs[2].grid(True)

# Adding labels for atmospheric layers
layers = [
    (0, 11, 'Troposphere'),
    (11, 20, 'Tropopause'),
    (20, 32, 'Stratosphere (1)'),
    (32, 47, 'Stratosphere (2)'),
    (47, 51, 'Stratopause'),
    (51, 71, 'Mesosphere (1)'),
    (71, 86, 'Mesosphere (2)')
]

for ax in axs:
    for layer in layers:
        ax.axhline(layer[0], color='black', linestyle='--', linewidth=0.5)
        ax.axhline(layer[1], color='black', linestyle='--', linewidth=0.5)
        ax.text(ax.get_xlim()[1] * 0.6, (layer[0] + layer[1]) / 2, layer[2], fontsize=9)

plt.tight_layout()
plt.show()
