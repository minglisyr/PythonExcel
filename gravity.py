import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

class GravitySimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("Earth-Moon 3D Gravity Simulation")

        self.G = 6.67430e-11  # Gravitational constant
        self.steps = 20000  # Number of simulation steps

        self.create_widgets()
        self.create_plot()

    def create_widgets(self):
        tk.Label(self.master, text="Earth Mass (kg):").grid(row=0, column=0)
        self.center_mass = tk.Entry(self.master)
        self.center_mass.insert(0, "5.97e24")  # Earth's mass
        self.center_mass.grid(row=0, column=1)

        tk.Label(self.master, text="Moon Mass (kg):").grid(row=1, column=0)
        self.particle_mass = tk.Entry(self.master)
        self.particle_mass.insert(0, "7.34e22")  # Moon's mass
        self.particle_mass.grid(row=1, column=1)

        tk.Label(self.master, text="Initial Distance (m):").grid(row=2, column=0)
        self.initial_distance = tk.Entry(self.master)
        self.initial_distance.insert(0, "3.844e8")  # Average Moon-Earth distance
        self.initial_distance.grid(row=2, column=1)

        tk.Label(self.master, text="Initial Velocity (m/s):").grid(row=3, column=0)
        self.initial_velocity = tk.Entry(self.master)
        self.initial_velocity.insert(0, "1022")  # Moon's average orbital velocity
        self.initial_velocity.grid(row=3, column=1)

        tk.Label(self.master, text="Time Step (seconds):").grid(row=4, column=0)
        self.time_step = tk.Entry(self.master)
        self.time_step.insert(0, "3600")  # Default: 1 hour
        self.time_step.grid(row=4, column=1)

        tk.Label(self.master, text="Inclination (degrees):").grid(row=5, column=0)
        self.inclination = tk.Entry(self.master)
        self.inclination.insert(0, "5.14")  # Moon's orbital inclination
        self.inclination.grid(row=5, column=1)

        tk.Button(self.master, text="Simulate", command=self.simulate).grid(row=6, column=0, columnspan=2)


    def create_plot(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)

    def simulate(self):
        try:
            center_mass = float(self.center_mass.get())
            initial_distance = float(self.initial_distance.get())
            initial_velocity = float(self.initial_velocity.get())
            self.dt = float(self.time_step.get())
            inclination = float(self.inclination.get()) * np.pi / 180  # Convert to radians

            # Initial conditions
            r = np.array([initial_distance, 0, 0])
            v = np.array([0, initial_velocity * np.cos(inclination), initial_velocity * np.sin(inclination)])

            self.trajectory = [r]

            for _ in range(self.steps):
                r_mag = np.linalg.norm(r)
                if r_mag == 0:
                    break  # Avoid division by zero
                a = -self.G * center_mass * r / r_mag**3
                v += a * self.dt
                r += v * self.dt
                self.trajectory.append(r)

            self.trajectory = np.array(self.trajectory)

            self.ax.clear()
            max_val = np.max(np.abs(self.trajectory)) * 1.1
            self.ax.set_xlim(-max_val, max_val)
            self.ax.set_ylim(-max_val, max_val)
            self.ax.set_zlim(-max_val, max_val)
            
            self.ax.set_xlabel('X position (m)')
            self.ax.set_ylabel('Y position (m)')
            self.ax.set_zlabel('Z position (m)')
            self.ax.set_title('Moon Orbit Around Earth (3D)')

            # Plot full orbit path
            self.ax.plot(self.trajectory[:, 0], self.trajectory[:, 1], self.trajectory[:, 2], 'r-', alpha=0.3, label='Moon Orbit')
            
            # Plot Earth
            self.earth = self.ax.scatter([0], [0], [0], color='blue', s=200, label='Earth')
            
            # Initialize Moon (will be updated in animation)
            self.moon = self.ax.scatter([], [], [], color='green', s=100, label='Moon')

            self.ax.legend()

            # Initialize frame counter for animation
            self.frame = 0
            
            # Start animation
            if hasattr(self.master, '_after_id'):
                self.master.after_cancel(self.master._after_id)
            
            self.update_animation()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_animation(self):
        if self.frame < len(self.trajectory):
            # Update Moon position
            self.moon._offsets3d = (self.trajectory[self.frame:self.frame+1, 0],
                                    self.trajectory[self.frame:self.frame+1, 1],
                                    self.trajectory[self.frame:self.frame+1, 2])
            
            self.ax.view_init(elev=20, azim=self.frame/100)  # Rotate view
            self.canvas.draw()
            self.frame += 1
            self.master._after_id = self.master.after(50, self.update_animation)
        else:
            self.frame = 0  # Reset for next simulation

root = tk.Tk()
app = GravitySimulation(root)
root.mainloop()