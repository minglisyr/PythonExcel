import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button

def plot_complex_functions():
    def f1(z):
        return 4 - z

    def f2(z):
        return 16 / z

    real = np.linspace(-5, 5, 100)
    imag = np.linspace(-5, 5, 100)
    real, imag = np.meshgrid(real, imag)
    z = real + 1j * imag

    values_f1 = f1(z)
    values_f2 = f2(z)

    global fig, ax
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface for |f1(z) - f2(z)|
    surf = ax.plot_surface(real, imag, np.abs(values_f1 - values_f2), cmap='viridis', alpha=0.7)

    # Plot the intersection contour
    ax.contour(real, imag, np.abs(values_f1 - values_f2), levels=[0], colors='r', linewidths=2)

    # Plot x+y=4 as a plane
    xx, yy = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))
    zz = np.zeros_like(xx)
    ax.plot_surface(xx, yy, zz, color='blue', alpha=0.3)

    # Plot the line x+y=4 on the xy-plane
    x_line = np.linspace(-5, 5, 100)
    y_line = 4 - x_line
    ax.plot(x_line, y_line, zs=0, color='blue', linewidth=2)

    intersection_points = [2 + 2*np.sqrt(3)*1j, 2 - 2*np.sqrt(3)*1j]
    for point in intersection_points:
        ax.scatter([point.real], [point.imag], [0], color='r', s=50)

    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_zlabel('|f1(z) - f2(z)|')
    ax.set_title('Intersection of x+y=4 and x*y=16 in the Complex Plane')
    
    # Add a color bar
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # Add text instructions
    fig.text(0.5, 0.02, 'Press x/y/z for views, Ctrl+x/y/z for flipped views', ha='center')

    # Set up key press event handler
    def on_key(event):
        if event.key == 'x':
            ax.view_init(elev=0, azim=-90)
        elif event.key == 'y':
            ax.view_init(elev=0, azim=0)
        elif event.key == 'z':
            ax.view_init(elev=90, azim=0)
        elif event.key == 'ctrl+x':
            ax.view_init(elev=0, azim=90)
        elif event.key == 'ctrl+y':
            ax.view_init(elev=0, azim=180)
        elif event.key == 'ctrl+z':
            ax.view_init(elev=-90, azim=0)
        fig.canvas.draw()

    fig.canvas.mpl_connect('key_press_event', on_key)

    # Add button for switching between perspective and orthographic projections
    ax_button = plt.axes([0.8, 0.9, 0.15, 0.05])
    button = Button(ax_button, 'Toggle Projection')

    is_perspective = True
    def toggle_projection(event):
        nonlocal is_perspective
        if is_perspective:
            ax.set_proj_type('ortho')
            button.label.set_text('To Perspective')
            is_perspective = False
        else:
            ax.set_proj_type('persp')
            button.label.set_text('To Orthographic')
            is_perspective = True
        fig.canvas.draw()

    button.on_clicked(toggle_projection)

    plt.show()

plot_complex_functions()
