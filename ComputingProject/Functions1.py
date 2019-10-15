"""A File containing the functions to be used in this programme"""

from pylab import *
from matplotlib import pyplot as plt
from InitialConditions import Kinematics, Mass
from ConstantsVariables import Variables

# Kinematics = [N particles, Nv Variables, Dimensions]
# Variables = [N, Nv, G, dt, nsteps,  epsilon]


def pvu(kinematics, variables):
    """A Function that steps the POSITION & VELOCITY along, this function
    returns the new position and new velocity for each step dt along the time"""

    stepv = kinematics[:, 1, :] + acceleration(Kinematics, Variables)[:, 2, :] * variables[3]  # Step the velocity along
    stepx = kinematics[:, 0, :] + stepv * variables[3]  # Step the position along
    Kinematics[:, 1, :] = stepv  # Update the position kinematics array
    Kinematics[:, 0, :] = stepx  # Update the velocity kinematics array

    return kinematics  # Returns the Kinematics variables, with the position and speed updated for one time step


def acceleration(kinematics, variables):
    """A Function to calculate the ACCELERATION on each particle, it returns the
    acceleration and updates the kinematics array"""

    forcesij = np.zeros((variables[0], variables[0], 3))  # A matrix holding all the forces
    for i in range(variables[0]):  # Looping through N particles investigating the forces on the i'th particle

        for j in range(i + 1, Variables[0]):  # Finding the force of the j'th particle on the i'th

            constantij = variables[2] * Mass[i] * Mass[j]
            riminusrj = kinematics[i, 0, :] - kinematics[j, 0, :]
            modulusriminusrj = (sum(riminusrj**2))**0.5
            cubemodulus = modulusriminusrj**3

            if modulusriminusrj ** 0.5 >= Variables[5]:
                forcesij[i, j, :] = constantij * riminusrj / cubemodulus  # All the forces of i on j
                forcesij[j, i, :] = -1.0 * forcesij[i, j, :]  # Short cut for the j'th effect on i
            else:
                forcesij[i, j, :] = constantij * riminusrj / (modulusriminusrj**2 + Variables[5]**2)**1.5
                forcesij[j, i, :] = -1.0 * forcesij[i, j, :]

        # Sum the forces:
        sumx = sum(forcesij[:, i, 0]) / Mass[i]
        sumy = sum(forcesij[:, i, 1]) / Mass[i]
        sumz = sum(forcesij[:, i, 2]) / Mass[i]

        kinematics[i, 2, :] = sumx, sumy, sumz  # The acceleration of the i'th particle out of N particles

    return kinematics[:, :, :]  # Returns the Kinematics variables, with the acceleration updated


def ke(velocityhistory, variables):
    """Takes the list of velocities for each step and each particle and returns the KE"""

    ke_for_each_step = np.zeros(variables[4])
    for s in range(variables[4]):
        ke_of_each_particle = np.zeros(variables[0])
        for n in range(variables[0]):
            v = sum(velocityhistory[n, s, :] ** 2)
            ke_of_each_particle[n] = 0.5 * Mass[n] * v
        ke_for_each_step[s] = sum(ke_of_each_particle)

    return ke_for_each_step


def pe(positionhistory, variables):  # Potential Energy Calculator
    """A Function to calculate the POTENTIAL ENERGY of the particle"""

    pehistory = np.zeros(variables[4])
    for s in range(variables[4]):
        r = positionhistory[:, s, :]

        listenergires = np.zeros(variables[0])  # Array to hold the potential energy of each particle
        potentialij = np.zeros((variables[0], variables[0]))  # Array holding potential of each particle on all others
        for i in range(variables[0]):  # Looping through N particles investigating the potential on the i'th particle

            for j in range(i + 1, variables[0]):  # Finding the potential of the j'th particle on the i'th

                constantij = variables[2] * Mass[i] * Mass[j]
                riminusrj = r[i, :] - r[j, :]
                separation = (riminusrj[0] ** 2 + riminusrj[1] ** 2 + riminusrj[2] ** 2) ** 0.5

                if separation >= Variables[5]:
                    potentialij[i, j] = constantij / separation  # All the potential of i on j
                else:
                    potentialij[i, j] = constantij / ((riminusrj[0]**2 + riminusrj[1]**2 + riminusrj[2]**2)**0.5 + variables[7]**2)

            # Sum the Potential:
            potentialisum = np.sum(potentialij[:, i])  # The sum of the potential for the i'th particles
            listenergires[i] = -1.0 * potentialisum

        pehistory[s] = sum(listenergires)
    return pehistory  # Returns the Kinematics variables, with the acceleration updated


def rootmeansquare(positionhistory, velocityhistory, variables):
    """Calculates the Root Mean Square Radius and Velocity of the cluster"""

    rmsrhistory = np.zeros(variables[4])  # Hold results for all steps along simulation
    rmsvhistory = np.zeros(variables[4])  # Hold results for all steps along simulation

    for s in range(variables[4]):

        r = positionhistory[:, s, :]
        v = velocityhistory[:, s, :]

        listradii = np.zeros(variables[0])
        listv = np.zeros(variables[0])

        for t in range(variables[0]):
            listradii[t] = sum(r[t, :]**2)
            listv[t] = sum(v[t, :]**2)

        rmsr = np.sqrt((1.0/variables[0])*(np.sum(listradii)))
        rmsv = np.sqrt((1.0/variables[0])*(np.sum(listv)))

        rmsrhistory[s] = rmsr
        rmsvhistory[s] = rmsv

    return rmsrhistory, rmsvhistory


def stepcalculator(variables):

    # Calculate mass and volume:
    volume = (4*np.pi*variables[6]**3)/3
    mass = sum(Mass)

    # Calculate density and hence can calculate the timescale for a collapse:
    density = mass/volume
    timescale = np.sqrt(1/(variables[2]*density))

    dt = 1000*timescale/variables[4]

    return dt


def velocitydispersion(positionhistory, velocityhistory, variables):
    """To generate the data required for a velocity dispersion profile"""
    r1 = positionhistory[:, -1, :]**2
    v1 = velocityhistory[:, -1, :]**2

    r2 = positionhistory[:, -20, :]**2
    v2 = velocityhistory[:, -20, :]**2

    r3 = positionhistory[:, -50, :]**2
    v3 = velocityhistory[:, -50, :]**2

    r4 = positionhistory[:, -80, :] ** 2
    v4 = velocityhistory[:, -80, :] ** 2

    r5 = positionhistory[:, -120, :] ** 2
    v5 = velocityhistory[:, -120, :] ** 2

    r6 = positionhistory[:, -160, :] ** 2
    v6 = velocityhistory[:, -160, :] ** 2

    r = (r1 + r2 + r3 + r4 + r5 + r6)/6
    v = (v1 + v2 + v3 + v4 + v5 + v6)/6

    radius = np.sqrt(np.sum(r, axis=1))
    velocity = np.sqrt(np.sum(v, axis=1))

    num_bins = 50
    x = bin_data(radius, velocity, num_bins)[0]
    y = bin_data(radius, velocity, num_bins)[1]

    cut = np.where(x < variables[6]*2.5)
    xnew = x[cut]
    ynew = y[cut]/(3600*24)  # Turn it into kilometers a second

    xnew2 = xnew[np.logical_not(np.isnan(xnew))]
    ynew2 = ynew[np.logical_not(np.isnan(xnew))]

    return xnew2, ynew2


def bin_data(x_data, y_data, num_bins):

    # To find the bin starts
    bin_start = np.linspace(np.min(x_data), np.max(x_data), num_bins, endpoint=False)
    mean_y = []
    mean_x = []

    for i in range(len(bin_start) - 1):

        cut = np.where(np.logical_and(x_data >= bin_start[i], x_data < bin_start[i+1]))

        mean_x.append(np.mean(x_data[cut]))
        mean_y.append(np.mean(y_data[cut]))

    mean_x = np.asarray(mean_x)
    mean_y = np.asarray(mean_y)

    return mean_x, mean_y




