import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint

def lotka_volterra(X, t, alpha, beta, delta, gamma):
    x, y = X
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

def simulate_predator_prey(alpha, beta, delta, gamma, x0, y0, t_max):
    t = np.linspace(0, t_max, 1000)
    X0 = [x0, y0]
    solution = odeint(lotka_volterra, X0, t, args=(alpha, beta, delta, gamma))
    return t, solution

class PredatorPreyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Predator-Prey Model Simulator")
        
        # Set up full-screen
        self.width = master.winfo_screenwidth()
        self.height = master.winfo_screenheight()
        master.geometry(f"{self.width}x{self.height}+0+0")
        
        # Configure the grid
        master.grid_columnconfigure(1, weight=1)
        master.grid_rowconfigure(0, weight=1)
        
        # Bind F11 to toggle full-screen
        master.bind('<F11>', self.toggle_fullscreen)
        master.bind('<Escape>', self.exit_fullscreen)
        
        self.is_fullscreen = True  # Start in full-screen mode

        self.create_input_frame()
        self.create_plot_frame()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.master.attributes("-fullscreen", False)
        return "break"

    def create_input_frame(self):     
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W))

        # Create input fields
        self.alpha = tk.DoubleVar(value=1.0)
        self.beta = tk.DoubleVar(value=0.1)
        self.delta = tk.DoubleVar(value=0.075)
        self.gamma = tk.DoubleVar(value=1.5)
        self.x0 = tk.DoubleVar(value=10)
        self.y0 = tk.DoubleVar(value=5)
        self.t_max = tk.DoubleVar(value=100)

        ttk.Label(input_frame, text="Prey growth rate (α):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.alpha, width=10).grid(row=0, column=1)

        ttk.Label(input_frame, text="Predation rate (β):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.beta, width=10).grid(row=1, column=1)

        ttk.Label(input_frame, text="Predator growth rate (δ):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.delta, width=10).grid(row=2, column=1)

        ttk.Label(input_frame, text="Predator death rate (γ):").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.gamma, width=10).grid(row=3, column=1)

        ttk.Label(input_frame, text="Initial prey population:").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.x0, width=10).grid(row=4, column=1)

        ttk.Label(input_frame, text="Initial predator population:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.y0, width=10).grid(row=5, column=1)

        ttk.Label(input_frame, text="Simulation time:").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.t_max, width=10).grid(row=6, column=1)

        ttk.Button(input_frame, text="Simulate", command=self.update_plot).grid(row=7, column=0, columnspan=2, pady=10)

    def create_plot_frame(self):
        plot_frame = ttk.Frame(self.master, padding="10")
        plot_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        self.fig, self.ax = plt.subplots(2, 2, figsize=(self.width/120, self.height/120))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    def update_plot(self):
        alpha = self.alpha.get()
        beta = self.beta.get()
        delta = self.delta.get()
        gamma = self.gamma.get()
        x0 = self.x0.get()
        y0 = self.y0.get()
        t_max = self.t_max.get()

        t, solution = simulate_predator_prey(alpha, beta, delta, gamma, x0, y0, t_max)
        prey, predator = solution.T

        for ax in self.ax.flat:
            ax.clear()

        self.ax[0, 0].plot(t, prey, 'g-', label='Prey')
        self.ax[0, 0].plot(t, predator, 'r-', label='Predator')
        self.ax[0, 0].set_xlabel('Time')
        self.ax[0, 0].set_ylabel('Population')
        self.ax[0, 0].set_title('Population over Time')
        self.ax[0, 0].legend()

        self.ax[0, 1].plot(prey, predator, 'b-')
        self.ax[0, 1].set_xlabel('Prey Population')
        self.ax[0, 1].set_ylabel('Predator Population')
        self.ax[0, 1].set_title('Phase Space')

        self.ax[1, 0].plot(t, prey, 'g-')
        self.ax[1, 0].set_xlabel('Time')
        self.ax[1, 0].set_ylabel('Prey Population')
        self.ax[1, 0].set_title('Prey Population over Time')

        self.ax[1, 1].plot(t, predator, 'r-')
        self.ax[1, 1].set_xlabel('Time')
        self.ax[1, 1].set_ylabel('Predator Population')
        self.ax[1, 1].set_title('Predator Population over Time')

        self.fig.suptitle(f'Predator-Prey Model (α={alpha:.2f}, β={beta:.2f}, δ={delta:.2f}, γ={gamma:.2f})')
        self.fig.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect parameter as needed
        self.canvas.draw()

root = tk.Tk()
app = PredatorPreyGUI(root)
root.mainloop()