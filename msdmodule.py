import numpy as np
from scipy.special import erf
from math import sqrt, pi, exp


# Define the parameters
numberLignes = 4
D = 0.5
numberSections = 16
meanParticles = 62.5
numSteps = 10000
numberParticles = 1000
tauDiff = 3.125

def cN(t, meanParticles, tauDiff):
    return meanParticles * ((sqrt(t/(tauDiff*pi)) * (exp(-tauDiff/t) - 1) + erf(sqrt(tauDiff/t))) ** 2)

def msd_analytic(number_sections, num_steps, section_length, D):
    msd_analytic = np.zeros(num_steps)
    for t in range(1,num_steps):
        msd_analytic[t] = 2 - 2 * cN(t, meanParticles, tauDiff)
    return msd_analytic

# Compute the msd_analytic function
msd = msd_analytic(numberSections, numSteps, numberLignes*D, D)
