"""An Explanation of how the arrays and variables are setup in this program"""

# Mass, m(i) /kilograms
# Position r(i) [metres, r = xi + yj +zk]
# Velocity v(i) [metres per second]
# Acceleration a(i) [metres^2 per second]
# Kinetic Energy T(i) [Joules]
# Potential Energy U(i) [Joules]
# Number of particles N
# Time interval (Leap) dt [seconds]
# Gravitational Constant
# Array Shape =  ([x1,y1,z1],[vx1,vy1,vz1],[ax1,ay1,az1]),
#                ([x2,y2,z2],[vx2,vy2,vz2],[ax2,ay2,az2]),
#                .....       .....         .....        .....
#                where x,y,z are positions, v's are velocities and where
#                a's are accelerations, F are forces and the number is
#                whichever particle it denotes.


# Solar System Initial conditions, in case I lose other info:
Kinematics[0, 0, :] = 0, 0, 0
Kinematics[0, 1, :] = 0, 0, 0
Kinematics[0, 2, :] = 0, 0, 0
Kinematics[1, 0, :] = 149.6*(10**6), 0, 0
Kinematics[1, 1, :] = 22137.74178, -2573558.657, 0
Kinematics[1, 2, :] = 0, 0, 0
Kinematics[2, 0, :] = -778.54*(10**6), 0, 0
Kinematics[2, 1, :] = -817.41, 1128172.083, 0
Kinematics[2, 2, :] = 0, 0, 0

# Mass = [1.9889*(10**30), 5.9724*(10**24),  1.8986*(10**27), 0.64171*(10**24)]

# rxsquared = (kinematics[i, 0, 0] - kinematics[j, 0, 0]) ** 2
# rysquared = (kinematics[i, 0, 1] - kinematics[j, 0, 1]) ** 2
# rzsquared = (kinematics[i, 0, 2] - kinematics[j, 0, 2]) ** 2
# cubemodulus = ((rxsquared + rysquared + rzsquared) ** 0.5) ** 3
"""
def ke(kinematics, variables):  # Kinetic Energy Calculator
    A Function to calculate the KINETIC ENERGY of the particle

    # The list to hold all the speeds
    kelist = np.zeros(variables[0])
    for k in range(variables[0]):
        # The speed of the k'th particle (here we convert from velocity to speed) :
        speed = np.sqrt(kinematics[k, 1, 0] ** 2 + kinematics[k, 1, 1] ** 2 + kinematics[k, 1, 2] ** 2)
        kelist[k] = 0.5*Mass[k]*(speed**2)

    kineticenergy = np.sum(kelist)/((1000**2)/(24*3600))

    return kineticenergy
"""

# # NOw we must write the data into excel so I can make nice graphs
# import xlwt
# from Animation import x, y, ke, pe, time
# from ConstantsVariables import Variables
# from InitialConditions import Mass
# import matplotlib.pyplot as plt
# from matplotlib.ticker import AutoMinorLocator
# import numpy as np
#
#
# energyinfo = np.loadtxt('IMBH0R1e.txt')
# print energyinfo
# print energyinfo[:, 0]
#
#
#
#
# V = Variables
# ax = plt.axes(xscale='log', yscale='')
# plt.plot(x, y, '.', ms=5, color="orange")
#
# ax.get_yaxis().set_tick_params(which='both', direction='in')
# ax.get_xaxis().set_tick_params(which='both', direction='in')
#
# v = np.sqrt(V[2]*sum(Mass))/x
# ax.yaxis.set_minor_locator(AutoMinorLocator(4))
#
# ax.tick_params(axis='both', which='minor', bottom='on')
# plt.ylabel('$\sigma$ [km/s]')
# plt.xlabel('R [parsecs]')
# plt.draw()
# plt.draw()
# plt.show()
