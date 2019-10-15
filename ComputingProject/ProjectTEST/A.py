"""A FILE to show an animation of the particles evolution with time"""

import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
from Functions1 import pe, kinetic, acceleration, pvu, timestepper, stepcalculator
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

for i in range(V[4]):
    positionhistory[:, i, :] = pvu(K, V)[:, 0, :]
    velocityhistory[:, i, :] = pvu(K, V)[:, 1, :]



# Build the figure:
df = positionhistory

fig = plt.figure()

# Set up the limits of the axes:
if V[8] == 1:
    axislimit = 1.1*V[6]
elif V[8] == 2:
    axislimit = 1.1 * V[6]
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
title = ax.set_title('3D Test')
data = df


graphs = []
for h in range(V[0]):
    if forshow == 1:
        graph, = ax.plot([data[h, 0, 0]], [data[h, 0, 1]], [data[h, 0, 2]], linestyle="",
                         marker="s", color="white", ms="1")
    else:
        graph, = ax.plot([data[h, 0, 0]], [data[h, 0, 1]], [data[h, 0, 2]], linestyle="", marker="o",
                         color="Blue", ms="1")

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
