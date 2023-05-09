import numpy as np
import pickle
# parameters
num_steps =10000
number_particles = 1000
dt = 0.1
c = 1
#boundry 
xmin=-10
xmax=10
ymin=-10
ymax=10
# Initializing steps 
nx = np.zeros((number_particles, num_steps))
ny = np.zeros((number_particles, num_steps))
#intializing positions
x = np.random.uniform(ymin,ymax,(number_particles, num_steps))
y = np.random.uniform(ymin,ymax,(number_particles, num_steps))

#creating data
nx = np.random.normal(loc=0.0, scale=1.0, size=(number_particles,num_steps-1))
ny = np.random.normal(loc=0.0, scale=1.0, size=(number_particles,num_steps-1))

for j in range(number_particles):
    for i in range(num_steps - 1):
        # using Euler method to update the equation
        x[j, i+1] = (x[j, i] + np.sqrt(c * dt) * nx[j, i] - xmin) % (xmax - xmin) + xmin
        y[j, i+1] = (y[j, i] + np.sqrt(c * dt) * ny[j, i] - ymin) % (ymax - ymin) + ymin
        
#saving them as a pickle table
data = {}

for j in range(number_particles):
    data[f'Particle_{j}'] = {'x': x[j, :], 'y': y[j, :]}
with open("particle_positions1.pkl", "wb") as f:
    pickle.dump([x,y], f)

