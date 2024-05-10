import numpy as np
import plotly.graph_objects as go


# Load data from the text file
data = np.loadtxt('dataset.txt')

# Assuming your data is organized as [x1, y1, z1; x2, y2, z2; ...]
x, y, z = data[:, 0], data[:, 1], data[:, 2]

# Create a 3D surface plot
fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='markers',marker=dict(size=5,color=z,colorscale='Blackbody',opacity=0.8)))

# Customize the plot (add labels, title, etc.)
fig.update_layout(
    scene=dict(
        xaxis_title='Q',
        yaxis_title='RPM',
        zaxis_title='dP',
        xaxis_range=[-45, 110],  # Set x-axis range
        yaxis_range=[80, 220],  # Set y-axis range
        zaxis_range=[-35, 15],  # Set z-axis range
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
    ),
    title='Interactive 3D Surface Plot',
)

# Show the interactive plot
fig.show()

def linear_interpolation(x0, y0, x1, y1, x2, y2, z1, z2):
    # Calculate the interpolated z value
    z0 = z1 + (z2 - z1) / (y2 - y1) * (y0 - y1)
    return z0

# Given (x0, y0) for interpolation
x0, y0 = 31.5, 165

# Find the indices of the nearest points (x1, y1) and (x2, y2)
idx1 = min(range(len(x)), key=lambda i: abs(x[i] - x0))
idx2 = max(0, idx1 - 1)

# Perform linear interpolation
z0 = linear_interpolation(x0, y0, x[idx1], y[idx1], x[idx2], y[idx2], z[idx1], z[idx2])

print(idx1,idx2)

print(f"Interpolated z0 at ({x0}, {y0}): {z0:.2f}")