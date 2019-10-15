"""A FILE to show an animation of the particles evolution with time"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
from Functions1 import pe, ke, pvu, stepcalculator, rootmeansquare, velocitydispersion
from InitialConditions import Kinematics, Mass, Variables


K = Kinematics
V = Variables
Mass = Mass


forshow = 0       # 0 means white background and axis, 1 is for display/look cool
if V[8] == 0:
        V[3] = 1
else:
    V[3] = stepcalculator(V)  # Set the time step to the right length

# Generate the data for the animation:
t = list(range(V[1]))
positionhistory = np.zeros((V[0], V[4], V[1]))
velocityhistory = np.zeros((V[0], V[4], V[1]))

# Generate the positions and velocities of all the particles:
for i in range(V[4]):
    positionhistory[:, i, :] = pvu(K, V)[:, 0, :]
    velocityhistory[:, i, :] = pvu(K, V)[:, 1, :]
print np.sqrt(sum(positionhistory[0, V[4]-1, :]**2))
print np.sqrt(sum(positionhistory[0, V[4]-1, :]**2))
print np.sqrt(sum(positionhistory[0, V[4]-1, :]**2))
print np.sqrt(sum(positionhistory[0, V[4]-1, :]**2))
print np.sqrt(sum(positionhistory[0, V[4]-1, :]**2))

# Generate the PE & KE data
time = np.linspace(0, V[4]*V[3]/(365*1000000), V[4])
ke = ke(velocityhistory, V)
pe = pe(positionhistory, V)


# plt.figure(2)
# plt.plot(time, ke, "orange")
# plt.plot(time, pe, "purple")
# plt.plot(time, pe + ke, "blue")
# plt.ylabel("Energy")
# plt.ylabel("Age (Million years")

plt.figure()
rmsr = rootmeansquare(positionhistory, velocityhistory, V)[0]
rmsv = rootmeansquare(positionhistory, velocityhistory, V)[1]
if V[8] == 2:
    np.savetxt('RMSr1BH2.txt', np.asarray([rmsr, rmsv]).T)
else:
    np.savetxt('RMSr12.txt', np.asarray([rmsr, rmsv]).T)

plt.plot(time, rmsr, "black")
plt.figure()
plt.plot(time, rmsv, "grey")
plt.ylabel("VRMS- Grey, RMSR- Black")


x = velocitydispersion(positionhistory, velocityhistory, V)[0]
y = velocitydispersion(positionhistory, velocityhistory, V)[1]



if V[8] == 2:   # With IMBH mass = 1000:
    np.savetxt('SBHR1e.txt', np.asarray([ke, pe, time]).T)
    np.savetxt('SBHR1v.txt', np.asarray([x, y]).T)
else:           # Without IMBH mass = 0:
    np.savetxt('SBH0R1e.txt', np.asarray([ke, pe, time]).T)
    np.savetxt('SBH0R1v.txt', np.asarray([x, y]).T)

# plt.figure(3)
# plt.plot(x, y, ".", ms="2")
# plt.ylabel('$\sigma$ [km/s]')

# Build the figure:
df = positionhistory/(3.086*10**13)

fig = plt.figure(1)

# Set up the limits of the axes:
if V[8] == 1:
    axislimit = 1.1*V[6]/(3.086*10**13)
elif V[8] == 2:
    axislimit = 1.1 * V[6]/(3.086*10**13)
else:
    axislimit = 8*(10**8)

# Set up the fig
if forshow == 1:
    ax = fig.add_subplot(111, projection='3d', facecolor="black")
else:
    ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(-1.0*axislimit, axislimit)
ax.set_ylim(-1.0*axislimit, axislimit)
ax.set_zlim(-1.0*axislimit, axislimit)
plt.xlabel('R [parsecs]')
plt.xticks(np.arange(-10, 10, 5))
plt.yticks(np.arange(-10, 10, 5))
title = ax.set_title('3D Test')
data = df


graphs = []
for h in range(V[0]):
    if forshow == 1:
        graph, = ax.plot([data[h, 0, 0]], [data[h, 0, 1]], [data[h, 0, 2]], linestyle="",
                         marker=".", color="white", ms="1")
    else:
        if h > 4:
            graph, = ax.plot([data[h, 0, 0]], [data[h, 0, 1]], [data[h, 0, 2]], linestyle="", marker="o", color="Black", ms="1")
        else:
            graph, = ax.plot([data[h, 0, 0]], [data[h, 0, 1]], [data[h, 0, 2]], linestyle="", marker="o", color="Red", ms="2")
    graphs.append(graph)


# Update the graph, includes title and such:
def update_graph(num):

    for m in range(V[0]):
        graph = graphs[m]
        data = df[m, num]
        graph.set_data(data[0], data[1])
        graph.set_3d_properties(data[2])
        title.set_text('Cluster Collapse, time = {} million years'.format(round(num*V[3]/(365*1000000), 1)))
    return title, graphs,


ani = matplotlib.animation.FuncAnimation(fig, update_graph, frames=np.arange(V[4]), interval=1, blit=False, )


if forshow == 1:
    plt.axis('off')

plt.show()





