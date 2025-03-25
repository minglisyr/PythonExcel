import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

def lorenz_system(state, t, sigma, rho, beta):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]

# Set parameters
sigma = 10
rho = 28
beta = 8/3

# Set initial conditions
initial_state = [1.0, 1.0, 1.0]

# Set time points
t = np.linspace(0, 100, 10000)

# Solve ODE
solution = odeint(lorenz_system, initial_state, t, args=(sigma, rho, beta))

# Extract x, y, z coordinates
x = solution[:, 0]
y = solution[:, 1]
z = solution[:, 2]

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Initialize the plot
line, = ax.plot([], [], [], lw=0.5)
point, = ax.plot([], [], [], 'ro', markersize=5)

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Lorenz Attractor')

# Set axis limits
ax.set_xlim(min(x), max(x))
ax.set_ylim(min(y), max(y))
ax.set_zlim(min(z), max(z))

# Animation update function
def update(frame):
    line.set_data(x[:frame], y[:frame])
    line.set_3d_properties(z[:frame])
    point.set_data([x[frame]], [y[frame]])
    point.set_3d_properties([z[frame]])
    return line, point

# Create animation
anim = FuncAnimation(fig, update, frames=range(0, len(x), 20), interval=50, blit=True, repeat=False)

# Show the plot
plt.show()

# Optionally, save the animation (uncomment the line below if you want to save it)
# anim.save('lorenz_attractor.gif', writer='pillow', fps=30)