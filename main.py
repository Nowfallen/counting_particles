#libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import math
from msdmodule import averaging
from msdmodule import total_average

# parameters
num_steps =200
number_particles = 100
dt = 0.01
c = 1
#boundry 
xmin=-10
xmax=10
ymin=-10
ymax=10
number_lignes=2
number_sections = int(math.pow(number_lignes, 2))
#we will just have to consider it to be cubes for now
section_length=(xmax-xmin)/number_lignes
# Initializing steps 
nx = np.zeros((number_particles, num_steps))
ny = np.zeros((number_particles, num_steps))
#intializing positions
x = np.random.uniform(ymin,ymax,(number_particles, num_steps))
y = np.random.uniform(ymin,ymax,(number_particles, num_steps))
# steps
for j in range(number_particles):
    for i in range(num_steps - 1):
        nx[j, i] = np.random.normal(0, 1)
        ny[j, i] = np.random.normal(0, 1)
        # using Euler method to update the equation
        x[j, i+1] = (x[j, i] + np.sqrt(c * dt) * nx[j, i] - xmin) % (xmax - xmin) + xmin
        y[j, i+1] = (y[j, i] + np.sqrt(c * dt) * ny[j, i] - ymin) % (ymax - ymin) + ymin
def Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    num_particles_insection = np.zeros((number_lignes**2, num_steps))
    for i in range(num_steps):
        for j in range(number_particles):
            xposition=int((x[j,i]-xmin)/section_length)
            yposition=int((y[j,i]-ymin)/section_length)
            num_particles_insection[xposition * number_lignes + yposition, i] += 1
    return num_particles_insection

#  the distribution difference  
def distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    number_sections = number_lignes**2
    distribution_diff = np.zeros((number_sections, num_steps))
    distribution_t0 = Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)[:,0]
    for t in range(1, num_steps):
        distribution_t = Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)[:,t-1]
        distribution_diff[:,t] = (distribution_t - distribution_t0)**2
    return distribution_diff
diff = distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)
# Plot the squared difference of particle distributions for each section
for i in range(number_sections):
    plt.plot(range(num_steps), diff[i])   
#the msd that will average on all sections
def computational_msd(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    computational_displacement = np.zeros(num_steps)
    for t in range(num_steps):
        computational_displacement[t] = np.mean(distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)[:, t])
    return computational_displacement
msd = computational_msd(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)
# the mean squared displacement plot
plt.plot(range(num_steps), msd,color="black")
plt.grid()
plt.show()
  
num_particles_insection = Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)


"""
# creating subplots for each section
fig, axes = plt.subplots(number_lignes, number_lignes, figsize=(7 * number_lignes, 7 * number_lignes), sharey=True)
for i_x in range(number_lignes):
    for i_y in range(number_lignes):
       
                  k = i_x * number_lignes + i_y
                  axes[i_x, i_y].bar(range(num_steps), num_particles_insection[k])
                  axes[i_x, i_y].set_xlabel("Number of steps")
                  axes[i_x, i_y].set_ylabel("Number of particles")
                  axes[i_x, i_y].set_title(f"xaxis {round(xmin + i_x * section_length,1) ,round(xmin + (i_x + 1) * section_length,1) } and yaxis {round(ymin + i_y * section_length,1) ,round(ymin + (i_y + 1) * section_length,1)}\n the average number of particles :{averaging(num_particles_insection,num_steps)[k]} ",color="blue")
                  axes[i_x, i_y].grid(color="Grey", linewidth="0.5", linestyle="-.")
                 


fig.suptitle(f"Number of particles in each section through time\n"
             f"The average number of particles in all the sections: {round(total_average(num_particles_insection, num_steps),1)}")

plt.show()
#in case we wwant to animate it to show us the particles moving and it calls a modulus to do so
#output_path = "/home/elaisati/2D animation.gif"
#animate_particles(x, y, num_steps,number_particles, xmin, xmax, ymin, ymax, output_path) """

