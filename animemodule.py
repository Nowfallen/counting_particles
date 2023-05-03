#creating a modulus to animate the particles
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter

def animate_particles(x, y, num_steps,number_particles, xmin, xmax, ymin, ymax, output_path):
    fig = plt.figure()

    # Creating a list of lines
    lines = [plt.plot([], [], marker="o", color="blue", markersize=5)[0] for _ in range(number_particles)]

    # Updating the animation
    def update(i):
        for j, line in enumerate(lines):
            line.set_data(x[j, i:i+1], y[j, i:i+1])
        return tuple(lines),

    ani = FuncAnimation(fig, update, frames=num_steps, interval=20, blit=False)
    number_of_lignes=3
    section_length_x=(xmax-xmin)/number_of_lignes
    section_length_y=(ymax-ymin)/number_of_lignes
    ax = plt.gca()
    ax.set_xticks([xmin,xmin+section_length_x,xmin+2*section_length_x,xmax])
    ax.set_yticks([ymin,ymin+section_length_y,ymin+2*section_length_y,ymax])
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    plt.xlabel("position X")
    plt.ylabel("position Y")
    plt.title("ols  (frame =10)(number of particles =100)")

    # Saving the anumation
    writer = PillowWriter(fps=10)
    ani.save(output_path, writer=writer)

    plt.show()
