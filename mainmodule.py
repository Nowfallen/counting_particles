import numpy as np
import math


def Distribution_data(x, y,data, section_lengthx,section_lengthy, num_steps, number_lignes):
    num_particles_insection_data= np.zeros((number_lignes**2, num_steps))
    for i in range(num_steps):
        for xvalue, yvalue in zip(x[data['frame']== i], y[data['frame'] == i]):
            xposition = int(xvalue / section_lengthx)
            yposition = int(yvalue / section_lengthy)
            xposition = min(xposition, number_lignes - 1)
            yposition = min(yposition, number_lignes - 1)
            num_particles_insection_data[xposition * number_lignes + yposition, i] += 1
    return num_particles_insection_data



def fluctuation_diff(x, y, section_lengthx,section_lengthy, num_steps, number_lignes,number_sections,num_particles_insection_data):
    fluctuation_diff = np.zeros((number_sections, num_steps))
    for delta in range(1,num_steps):
        nt0 = 0
        for t0 in range (0, num_steps-delta):
            fluctuation_t0 = num_particles_insection_data[:,t0]
            fluctuation_t = num_particles_insection_data[:,t0 + delta]
            fluctuation_diff[:,delta] += (fluctuation_t - fluctuation_t0)**2
            nt0 += 1
        fluctuation_diff[:,delta] /= nt0
    return fluctuation_diff

def computational_msd(diff, num_steps):
    computational_displacement = np.zeros(num_steps)
    for t in range(num_steps):
        computational_displacement[t] = np.mean(diff[:, t])
    return computational_displacement
