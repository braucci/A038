import numpy as np
import matplotlib.pyplot as plt

def naca4(m, p, t, c=1, num_points=1000):

    """
    Author: Raucci Biagio
    Scope: The code generates the coordinates for a NACA 4-series airfoil.
    Date: 2021-07-01
    Last Modified: 2021-07-01

    Generate the coordinates for a NACA 4-series airfoil.
    
    Parameters:
    m (float): Maximum camber (in % of the chord length)
    p (float): Position of maximum camber (in tenths of the chord length)
    t (float): Maximum thickness (in % of the chord length)
    c (float): Chord length (default is 1)
    num_points (int): Number of points to generate
    
    Returns:
    x (ndarray): x-coordinates
    y_upper (ndarray): y-coordinates of the upper surface
    y_lower (ndarray): y-coordinates of the lower surface
    """
    x = np.linspace(0, c, num_points)
    yt = (t / 0.20) * c * (0.2969 * np.sqrt(x / c) - 0.1260 * (x / c) - 0.3516 * (x / c)**2 + 0.2843 * (x / c)**3 - 0.1015 * (x / c)**4)
    
    if p == 0:
        yc = np.zeros_like(x)
        dyc_dx = np.zeros_like(x)
    else:
        yc = np.where(x <= p * c,
                      (m / p**2) * (2 * p * (x / c) - (x / c)**2),
                      (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * (x / c) - (x / c)**2))
        dyc_dx = np.where(x <= p * c,
                          (2 * m / p**2) * (p - x / c),
                          (2 * m / (1 - p)**2) * (p - x / c))

    theta = np.arctan(dyc_dx)
    
    y_upper = yc + yt * np.cos(theta)
    y_lower = yc - yt * np.cos(theta)
    
    return x, y_upper, y_lower

def plot_naca4(m, p, t, c=1):
    x, y_upper, y_lower = naca4(m, p, t, c)
    
    plt.figure(figsize=(10, 5))
    plt.plot(x, y_upper, 'b', label='Upper Surface')
    plt.plot(x, y_lower, 'r', label='Lower Surface')
    plt.plot(x, np.zeros_like(x), 'k--', label='Chord Line')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'NACA {int(m*100):01}{int(p*10):01}{int(t*100):02}')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# Example usage:
# NACA 0012 profile (m=0.0, p=0.0, t=0.12)
NACA = "0012"  # Use a string to preserve leading zeros

# Extract m, p, and t from the string
m = int(NACA[0]) / 100
p = int(NACA[1]) / 10
t = int(NACA[2:]) / 100

plot_naca4(m, p, t)
