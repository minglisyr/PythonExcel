import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# load the file
xyz = np.genfromtxt('dataset-KB30.txt')

# Define the query point (VFRq,RPMq)
VFRq = 30
RPMq = 150

# Define the plot ranges
dx = round((np.max(xyz[:, 0]) - np.min(xyz[:, 0])) / 20)
dy = round((np.max(xyz[:, 1]) - np.min(xyz[:, 1])) / 20)
dz = round((np.max(xyz[:, 1]) - np.min(xyz[:, 1])) / 20)

VFRmin = dx * (round(np.min(xyz[:, 0]) / dx) - 1)
VFRmax = dx * (round(np.max(xyz[:, 0]) / dx) + 1)

RPMmin = dy * (round(np.min(xyz[:, 1]) / dy) - 1)
RPMmax = dy * (round(np.max(xyz[:, 1]) / dy) + 1)
dPmin = dz * (round(np.min(xyz[:, 2]) / dz) - 1)
dPmax = dz * (round(np.max(xyz[:, 2]) / dz) + 1)

# Create a 2D interpolator to calculate the z-value at any position
interp = interpolate.CloughTocher2DInterpolator(xyz[:,:2], xyz[:,2])
Zq = interp(VFRq, RPMq)

# Plot
fig, ax = plt.subplots(figsize=[12, 8])  # Create a single subplot

# Override the format_coord method to display x, y, and z values
def fmt(x, y):
    z = interp(x, y).item()
    return f'x={x:.5f}  y={y:.5f}  z={z:.5f}'

ax.format_coord = fmt

# Scatter plot with tricontourf
cb = ax.tricontourf(xyz[:, 0], xyz[:, 1], xyz[:, 2], levels=20, vmin=dPmin, vmax=dPmax)
plt.colorbar(cb, ax=ax, label='dP (bar)')
ax.set_xlim(VFRmin, VFRmax)
ax.set_ylim(RPMmin, RPMmax)

# Set axis ticks and labels
ax.set_xticks(np.arange(VFRmin, VFRmax, dx))
ax.set_yticks(np.arange(RPMmin, RPMmax, dy))
ax.set_xlabel('VFR (cm^3/s)')
ax.set_ylabel('RPM')

# Scatter the original data points
ax.scatter(xyz[:,0], xyz[:,1], color='black', alpha=.5, s=30, marker='x')

ax.set_title('dP surface')

plt.show()
