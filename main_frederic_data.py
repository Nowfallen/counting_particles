#libraries
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from msdmodule import f_msd
from msdmodule import another_function
import pandas as pd 
from lmfit import Model, Parameters
#boundry 
xmin=0
xmax=2560
ymin=0
ymax=2160
#Data
data = pd.read_csv('Exp2_tracks.csv')
num_steps =data['frame'].unique()
x = data['x']
y = data['y']
num_particles = len(data['particle_id'].unique())
dt=np.mean(np.diff(num_steps))
maxDuration = 100
steps=data['frame'].nunique()


#computing
def compute_r(x, y, num_particles, num_steps):
    rsquared = np.zeros((num_particles, maxDuration))
    #locating the data
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

model= Model(f_msd)
params=Parameters()

params.add('D',vary=True,min=0.000001)

# ADDING WEIGHTS , WHERE THE FIRST DATA  IS MORE IMPORTANT THAN THE LAST ONE 
weights1 = (maxDuration-np.arange(1,maxDuration))/ (maxDuration*(maxDuration+1)/2)
weights2 = np.diff(np.log(range(1,maxDuration)))
weights2=np.append(weights2,weights2[-1])

result = model.fit(msd[1:maxDuration], params, weights=weights2*weights1, t=range(1, maxDuration))
print(result.fit_report())


plt.loglog(range(1, maxDuration), msd[1:steps],'.', color="blue", label=" Data")

plt.loglog(range(1,maxDuration),result.best_fit,color='black',label=r'$f_{\mathrm{msd}} = 4Dt$')

plt.grid()
plt.legend()
plt.xlabel("frames[dt=34.6ms]")
plt.ylabel("displacement [pixels]")
plt.title('Mean squared displacement Method\n the Diffusion Coefficient is $D=0.1268\, \mu m^2/s$', color='black')
plt.show()

"""  
   for i in range(len(x)):
       if data.particle_id[i] == ipart:
           indices.append(i)
   xpart = np.array([x[ind] for ind in indices])
   ypart = np.array([y[ind] for ind in indices]"""
