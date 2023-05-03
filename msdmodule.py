import numpy as np
import math




# the msd equation 2-2*correlation(i think i should add intial time so i can average over it):
def msd(num_particles_insection, number_sections, t, section_length, D):
    return 2 - 2 * cN(t, num_particles_insection, number_sections, section_length, D)





#the correlation equation:
def cN(t, num_particles_insection, number_sections, section_length, D):
    return averaging(num_particles_insection, num_steps)* (np.sqrt(t/ (toudiff(section_length, D) * np.pi)) * (np.exp(-toudiff_value/t)- 1)) + math.erf(np.sqrt(toudiff(section_length, D) / t))



#average number of particles in a particular section:
def averaging(num_particles_insection, num_steps):
    num_sections = num_particles_insection.shape[0]
    average_number_section = np.zeros(num_sections)
    for i in range(num_sections):
        average_number_section[i] = np.sum(num_particles_insection[i]) / num_steps
    return average_number_section

#the total average :
def total_average(num_particles_insection, num_steps):
    num_sections = num_particles_insection.shape[0]
    return np.sum(averaging(num_particles_insection,num_steps))/num_sections

 
#time the particle takes to diffuse in one section:
def toudiff(section_length, D):
    return (section_length ** 2) / (4 * D)
