import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Dati forniti
W = 13127.5  # peso in N
rho = 1.225  # densità dell'aria in kg/m^3
S = 16.165  # area alare in m^2
b = 10.912  # apertura alare in m
e = 0.8  # fattore di efficienza di Oswald
C_D0 = 0.025  # coefficiente di resistenza a portanza nulla

# Calcolo del rapporto d'aspetto
AR = b**2 / S

# Funzione per calcolare le proprietà aerodinamiche
def calculate_aero_properties(V_inf):
    CL = W / (0.5 * rho * V_inf**2 * S)
    CD = C_D0 + (CL**2) / (np.pi * e * AR)
    L_D = CL / CD
    TR = W / L_D
    return CL, CD, L_D, TR

# Velocità per il calcolo
# V_inf_values = [30.48, 45.72, 76.2, 91.44, 106.68]
V_inf_values = np.linspace(30.48, 106.68, 100)

# Liste per memorizzare i risultati
CL_values = []
CD_values = []
L_D_values = []
TR_values = []

# Calcolo delle proprietà per ogni velocità
for V_inf in V_inf_values:
    CL, CD, L_D, TR = calculate_aero_properties(V_inf)
    CL_values.append(CL)
    CD_values.append(CD)
    L_D_values.append(L_D)
    TR_values.append(TR)

# Creazione della tabella
data = {
    'V_inf (m/s)': V_inf_values,
    'CL': CL_values,
    'CD': CD_values,
    'L/D': L_D_values,
    'TR (N)': TR_values
}
df = pd.DataFrame(data)

# Mostra la tabella
#print(df)

# Grafico della spinta richiesta in funzione della velocità di volo
plt.figure(figsize=(10, 6))
plt.plot(V_inf_values, TR_values, marker='o', linestyle='-', color='b')
plt.xlabel('V_inf (m/s)')
plt.ylabel('TR (N)')
plt.title('Thrust Required (TR) vs. Flight Velocity (V_inf)')
plt.grid(True)
plt.show()
