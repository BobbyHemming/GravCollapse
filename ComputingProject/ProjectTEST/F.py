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


def kinetic(kinematics):

    velocity = kinematics[:, 1, :]

    v = velocity**2

    sumv = np.sum(v, axis=1)
    kenergy = 0.5*Mass*sumv # 0.5*Mass*

    totalke = np.sum(kenergy)

    return totalke


def pe(kinematics, variables):  # Potential Energy Calculator
    """A Function to calculate the POTENTIAL ENERGY of the particle"""

    listenergires = np.zeros(variables[0])  # Array to hold the potential energy of each particle
    potentialij = np.zeros((variables[0], variables[0]))  # Array to hold the potential of each particle on one another
    for i in range(variables[0]):  # Looping through N particles investigating the potential on the i'th particle

        for j in range(i + 1, variables[0]):  # Finding the potential of the j'th particle on the i'th

            constantij = variables[2] * Mass[i] * Mass[j]
            riminusrj = kinematics[i, 0, :] - kinematics[j, 0, :]
            separation = (riminusrj[0] ** 2 + riminusrj[1] ** 2 + riminusrj[2] ** 2) ** 0.5

            if separation >= Variables[5]:
                potentialij[i, j] = constantij / separation  # All the potential of i on j
            else:
                potentialij[i, j] = constantij / ((riminusrj[0]**2 + riminusrj[1]**2 + riminusrj[2]**2)**0.5 + variables[7]**2)

        # Sum the Potential:
        potentialisum = np.sum(potentialij[:, i])  # The sum of the potential for the i'th particles
        listenergires[i] = -1.0 * potentialisum

    potentialsum = sum(listenergires)

    return potentialsum  # Returns the Kinematics variables, with the acceleration updated


def virialradius(kinematics, variables):
    """Calculates the Virial Radius of the cluster"""

    history = np.zeros(variables[0])
    separationhistory = np.zeros(variables[0])

    for i in range(variables[0]):
        x = (kinematics[i, 0, 0] ** 2 + kinematics[i, 0, 1] ** 2 + kinematics[i, 0, 2] ** 2) ** 0.5
        m = Mass[i]
        history[i] = x * m
    xcm = sum(history) / sum(Mass)

    for n in range(variables[0]):
        r = (kinematics[i, 0, 0] ** 2 + kinematics[i, 0, 1] ** 2 + kinematics[i, 0, 2] ** 2) ** 0.5
        separationhistory[n] = r - xcm

    radius = sum(separationhistory)/variables[0]

    return (radius**2)**0.5


def rootmeansquare(kinematics, variables):
    """Calculates the Root Mean Square Radius and Velocity of the cluster"""

    listradii = np.zeros(variables[0])
    listv = np.zeros(variables[0])

    for t in range(variables[0]):
        listradii[t] = (kinematics[t, 0, 0]**2 + kinematics[t, 0, 1]**2 + kinematics[t, 0, 2]**2)
        listv[t] = (kinematics[t, 1, 0] ** 2 + kinematics[t, 1, 1] ** 2 + kinematics[t, 1, 2] ** 2)

    rmsr = np.sqrt((1.0/variables[0])*(np.sum(listradii)))
    rmsv = np.sqrt((1.0/variables[0])*(np.sum(listv)))

    return rmsr, rmsv


def stepcalculator(variables):

    # Calculate mass and volume:
    volume = (4*np.pi*variables[6]**3)/3
    mass = sum(Mass)

    # Calculate density and hence can calculate the timescale for a collapse:
    density = mass/volume
    timescale = np.sqrt(1/(variables[2]*density))

    dt = timescale/variables[4]

    return dt


def velocitydispersion(kinematics, variables):
    """To generate the data required for a velocity dispersion profile"""

