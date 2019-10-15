import numpy as np
import random
from ConstantsVariables import Variables



Kinematics = np.zeros((Variables[0], Variables[1], 3))
Mass = np.zeros((Variables[0]))


def randomcluster(variables, mass):
    """A Function to generate the initial conditions (a set of kinematics and mass values) that can be used to
    simulate a cluster. Particles are randomly placed in a sphere with a square weighting"""

    kinematics = np.zeros((variables[0], variables[1], 3))

    count = 0
    while count < variables[0]:

        m = np.random.random()
        n = np.random.random()
        o = np.random.random()

        if m <= 0.5:
            r = -1
        else:
            r = 1
        if n <= 0.5:
            s = -1
        else:
            s = 1
        if o <= 0.5:
            t = -1
        else:
            t = 1

        x = r*variables[6] * (random.random()**2)
        y = s*variables[6] * (random.random()**2)
        z = t*variables[6] * (random.random()**2)

        vx = variables[7] * random.uniform(-1, 1)
        vy = variables[7] * random.uniform(-1, 1)
        vz = variables[7] * random.uniform(-1, 1)


        square = (x**2 + y**2 + z**2)**0.5

        if square <= variables[6]:

            kinematics[count, 0, 0] = x
            kinematics[count, 0, 1] = y
            kinematics[count, 0, 2] = z

            kinematics[count, 1, 0] = vx
            kinematics[count, 1, 1] = vy
            kinematics[count, 1, 2] = vz

            count = count + 1

        mass[count-1] = random.uniform(1, 1)*3*(10 ** 30)

    if variables[8] == 2:
        kinematics[0, 0, :] = [0, 0, 0]
        kinematics[0, 1, :] = [0, 0, 0]
        kinematics[0, 2, :] = [0, 0, 0]
        mass[0] = random.uniform(100, 1000)*(10 ** 30)

    return kinematics


def solarsystem(variables, orbitalconditions, mass):
    """A Function to generate the initial conditions (a set of kinematics and mass values) that can be used to
    simulate the solar system. Solar system parameters are setup in Constants and variables"""

    kinematics = np.zeros((variables[0], variables[1], 3))

    for i in range(3):

        mass[i] = orbitalconditions[i][0]

        if orbitalconditions[i][1] == 0:
            speed = 0
            angle = 0
        else:
            speed = np.sqrt(variables[2]*orbitalconditions[0][0]/(orbitalconditions[i][1]**2)**0.5)
            angle = variables[3]*speed/(2*orbitalconditions[i][1])

        # Positions:
        kinematics[i, 0, 0] = orbitalconditions[i][1]

        # Velocities:
        if orbitalconditions[i][1] >= 0:
            kinematics[i, 1, 0] = speed*np.sin(angle)
            kinematics[i, 1, 1] = -1.0*speed*np.cos(angle)
        else:
            kinematics[i, 1, 0] = -1.0*speed*np.sin(angle)
            kinematics[i, 1, 1] = speed*np.cos(angle)

    return kinematics


# Kinematics = randomcluster(Variables, Mass) or ...
# Kinematics = solarsystem(Variables, Orbitconditions, Mass)


if Variables[8] == 0:
    Kinematics = solarsystem(Variables, Orbitconditions, Mass)
else:
    Kinematics = randomcluster(Variables, Mass)
