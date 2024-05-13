import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

# load the file
xyz = np.genfromtxt('dataset.txt')

# Define the query point (VFRq,RPMq)
VFRq= 10
RPMq= 160

#Define the plot ranges
VFRmin=-45
VFRmax=105
RPMmin=90
RPMmax=215
dPmin=-35
dPmax=15

# Create a 2D interpolator to calculate the intenisity at any position
interp = scipy.interpolate.CloughTocher2DInterpolator(xyz[:,:2], xyz[:,2])
Zq=interp(VFRq,RPMq)

# Plot
fig, ax = plt.subplots(figsize=[16, 8])  # Create a single subplot


# Override the format_coord method to display x, y, and z values
def fmt(x, y):
    z = np.take(interp(x, y), 0)
    return f'x={x:.5f}  y={y:.5f}  z={z:.5f}'

plt.gca().format_coord = fmt

# Scatter plot with tricontourf
cb = ax.tricontourf(xyz[:, 0], xyz[:, 1], xyz[:, 2], levels=20, vmin=dPmin, vmax=dPmax)
plt.colorbar(cb, ax=ax, label='dP (bar)')
plt.axis([VFRmin,VFRmax,RPMmin,RPMmax])  # Adjust axis limits as needed

# Plot the query point with its Z-value
plt.plot(VFRq, RPMq, 'ok') 
plt.annotate(f'dP ={Zq:.2f} \n @(VFR= {VFRq:.2f},RPM={RPMq:.0f})', xy=(VFRq, RPMq), xytext=(VFRq + 1, RPMq + 1), color='black')

# Draw dashed lines to X and Y axes
plt.plot([VFRq, VFRq], [RPMq, RPMmin], linestyle='--', color='gray')
plt.plot([VFRq, VFRmin], [RPMq, RPMq], linestyle='--', color='gray')

# Scatter the original data points
ax.xaxis.set_ticks(np.arange(VFRmin, VFRmax, 5))
ax.yaxis.set_ticks(np.arange(RPMmin, RPMmax, 30))
ax.set_xlabel('VFR (cm^3/s)')
ax.set_ylabel('RPM')
ax.scatter(xyz[:,0], xyz[:,1], color='black', alpha=.5, s=30, marker='x')
    
    
ax.set_title('dP surface')

plt.show()