#libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, PillowWriter
import math
from msdmodule import msd_analytic
import pickle

# parameters
num_steps =1000
n=1
number_particles = 1000
#boundry 
xmin=0
xmax=20
ymin=0
ymax=20
number_lignes=25
D=0.5
number_sections = int(math.pow(number_lignes, 2))
pmax=int(num_steps/n)
#we will just have to consider it to be cubes for now
section_length=(xmax-xmin)/number_lignes
meanParticles=number_particles/number_sections
tauDiff= ((xmax-xmin)**2)/4*D

#opening the pickle file 
with open('particle_positions1.pkl', 'rb') as f:
    x,y= pickle.load(f)
#counting particles in each sub_space
def fluctuations(x, y, xmin, ymin, section_lengthx,section_lengthy, num_steps, number_particles, number_lines):
    num_particles_insection = np.zeros((number_lines**2, num_steps))
    for i in range(num_steps):
        for j in range(number_particles):
            xposition = int((x[j, i]) / section_lengthx)
            yposition = int((y[j, i]) / section_lengthy)
            num_particles_insection[xposition * number_lines + yposition, i] += 1
    return num_particles_insection
num_particles_insection =fluctuations (x, y, xmin, ymin, section_lengthx,section_lengthy, num_steps, number_particles, number_lines)

#  the distribution difference  sqr
def distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    distribution_diff = np.zeros((number_sections, num_steps))
    for delta in range(1, num_steps): 
        for t0 in range (1, num_steps): 
            distribution_t0 = num_particles_insection[:,t0]
            if t0 + n*delta < num_particles_insection.shape[1]:
                distribution_t = num_particles_insection[:,t0 + delta]
            distribution_diff[:,delta] += (distribution_t - distribution_t0)**2
        distribution_diff[:,delta] /= pmax
    return distribution_diff

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
msd_anly=msd_analytic( meanParticles,tauDiff,number_sections, num_steps, section_length, D)

time = np.arange(num_steps)
rescaled_timesteps = time * tauDiff
plt.loglog(range(num_steps), msd, '+', color="black", label="the mean")
plt.loglog(range(num_steps), msd_anly, color='blue', label='analytic mean')
plt.grid()
plt.legend()
plt.xlabel("time ")
plt.ylabel("number of flactuations")
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
#animate_particles(x, y, num_steps,number_particles, xmin, xmax, ymin, ymax, output_path) 

"""

#computing msd
def compute_r(x, y, num_particles, num_steps):
    rsquared = np.zeros((num_particles, maxDuration))
    #locating the data
    nt1=0
    for ipart in range(1, num_particles):
        # figure out which indices correspond to particle ipart
        indices = np.where(data['particle_id'] == ipart)[0]
        xpart= x.iloc[indices].values
        ypart = y.iloc[indices].values
        indices = []
        for delta in range(1, maxDuration):
            nt0 = 0
            for t0 in range(0, maxDuration - delta ):
                #print(t0)
                displacement_x0 = xpart[t0]
                displacement_x = xpart[t0 + delta]
                displacement_y0 = ypart[t0]
                displacement_y = ypart[t0 + delta]
                rsquared[ipart,delta] += (((displacement_x - displacement_x0) ** 2)+((displacement_y- displacement_y0) ** 2))
                nt0 += 1
            rsquared[ipart, delta]  /= (nt0)
    return rsquared
rseq = compute_r(x, y, num_particles, num_steps)
def computational_msd(rseq, maxDuration,num_particles):
    computational_displacement = np.zeros(maxDuration)
    for t in range(1,maxDuration):
        computational_displacement[t] = np.mean(rseq[:, t])
    return computational_displacement
msd = computational_msd(rseq, maxDuration,num_particles)
