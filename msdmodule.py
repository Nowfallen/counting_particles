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

#mean squar displacement <N(p,t)-N(p,0)>^2):
def computational_msd(number_particles, num_steps):
    computational_displacement = np.zeros(num_steps)
    for t in range(1, num_steps):
        squared_difference = (Distribution(x, y, xmin, ymin, section_length, t, number_particles, number_lignes) - Distribution(x, y, xmin, ymin, section_length, 0, number_particles, number_lignes))**2
        computational_displacement[t] = np.mean(squared_difference)
    return computational_displacement


#the total average :
def total_average(num_particles_insection, num_steps):
    num_sections = num_particles_insection.shape[0]
    return np.sum(averaging(num_particles_insection,num_steps))/num_sections

 
#time the particle takes to diffuse in one section:
def toudiff(section_length, D):
    return (section_length ** 2) / (4 * D)

def distribution_diff(x, y, xmin, ymin, section_length, num_steps, number_particles, number_lignes):
    number_sections = number_lignes**2
    distribution_diff = np.zeros((number_sections, num_steps))
    distribution_t0 = Distribution(x, y, xmin, ymin, section_length, 1, number_particles, number_lignes)
    for t in range(1, num_steps):
        distribution_t = Distribution(x, y, xmin, ymin, section_length, t + 1, number_particles, number_lignes)
        distribution_diff[:, t - 1] = (distribution_t[:, t] - distribution_t0[:, 0])**2
    return distribution_diff
