#libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import math
from msdmodule import msd_analytic
import pickle

# parameters
num_steps =10000
number_particles = 1000
#boundry 
xmin=-10
xmax=10
ymin=-10
ymax=10
number_lignes=2
D=5
number_sections = int(math.pow(number_lignes, 2))
#we will just have to consider it to be cubes for now
section_length=(xmax-xmin)/number_lignes

#opening the pickle file 
with open('particle_positions1.pkl', 'rb') as f:
    x,y= pickle.load(f)
#counting particles in each section
def Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    num_particles_insection = np.zeros((number_lignes**2, num_steps))
    for i in range(num_steps):
        for j in range(number_particles):
            xposition=int((x[j,i]-xmin)/section_length)
            yposition=int((y[j,i]-ymin)/section_length)
            num_particles_insection[xposition * number_lignes + yposition, i] += 1
    return num_particles_insection
num_particles_insection = Distribution(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)

#  the distribution difference  sqr
def distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    distribution_diff = np.zeros((number_sections, num_steps))
    distribution_0= num_particles_insection[:,0]
    for t in range(1, num_steps):
        distribution_t = num_particles_insection[:,t-1] 
        #the code 
        for k in range (1,t):
                  distribution_t0=np.mean(num_particles_insection[:,k-1])
                  distribution_diff[:,t] =(distribution_t-distribution_t0)**2
    return distribution_diff
diff = distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes)
#plotting it
for i in range(number_sections):
    plt.plot(range(num_steps), diff[i]) 
#the msd that will average on all sections
def computational_msd(diff, num_steps):
    computational_displacement = np.zeros(num_steps)
    for t in range(num_steps):
        computational_displacement[t] = np.mean(diff[:, t])     
    return computational_displacement

msd = computational_msd(diff, num_steps)
msd_anly=msd_analytic(num_particles_insection, number_sections, num_steps, section_length, D)
# Plot the msd
plt.plot(range(num_steps), msd,color="black",label="the mean")
plt.plot(range(num_steps),msd_anly,'--',color='purple',label='analytic mean')
plt.grid()
plt.legend()
plt.xlabel("number of steps")
plt.ylabel("displacement sqr value of distribution ")
plt.title('msd :distribution of particles in the observed space', color='blue')
plt.show()
  


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
