
from ConstantsVariables import Variables
from InitialConditions import Mass
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
import matplotlib
from ConstantsVariables import Variables
import seaborn as sns

energyinfo = np.loadtxt('IMBH0R1e.txt')
velocityinfo = np.loadtxt('IMBH0R1v.txt')

energy2info = np.loadtxt('IMBH1000R1e.txt')
velocity2info = np.loadtxt('IMBH1000R1v.txt')

RMSRr1BH = np.loadtxt('RMSr1BH.txt')[:, 0]
RMSVr1BH = np.loadtxt('RMSr1BH.txt')[:, 1]/(3600*24)

RMSRr1 = np.loadtxt('RMSr1.txt')[:, 0]
RMSVr1 = np.loadtxt('RMSr1.txt')[:, 1]/(3600*24)


energy = np.loadtxt('SBHR1e.txt')
position = np.loadtxt('RMSr1BH2.txt')/(3600*24)
time2 = energy[:, 2]
time = energyinfo[:, 2]

# IMBH mass = 0
ke1 = energyinfo[:, 0]
pe1 = energyinfo[:, 1]
x1 = velocityinfo[:, 0]/(3.086*10**13)
y1 = velocityinfo[:, 1]

# IMBH mass = 1000
ke2 = energy2info[:, 0]
pe2 = energy2info[:, 1]
x2 = velocity2info[:, 0]/(3.086*10**13)
y2 = velocity2info[:, 1]

# SMBH mass = 40*5
keS = energy[:, 0]
peS = energy[:, 1]
SMBHv = position[:, 1]
SMBHr = 3600*24*position[:, 0]/(3.086*10**13)

def polyfitter(x, y, deg):
    c = np.polyfit(x, y, deg)

    xnew = np.linspace(0, max(x1))
    # yhistory = np.zeros((len(xnew), deg+1))
    # ynew = np.zeros(len(x))
    # for i in range(deg+1):
    #     for n in range(len(xnew)):
    #         yhistory[n, i] = c[i]*xnew[n]**(deg+1-i)
    #     ynew[i] = sum(yhistory[:, i])

    yminus = c[0]*xnew**4
    yzero = c[1]*xnew**3
    yone = c[2]*xnew**2
    ytwo = c[3]*xnew
    ythree = c[4]

    ynew = yone + ytwo + ythree + yzero + yminus

    return xnew, ynew


plt.figure(1)

ax = plt.axes(xscale='log', yscale='')
plt.plot(polyfitter(x1, y1, 4)[0], polyfitter(x1, y1, 4)[1], color="blue", label='No IMBH', linewidth=1)
plt.plot(polyfitter(x2, y2, 4)[0], polyfitter(x2, y2, 4)[1], color="red", label='IMBH $1000M_{\odot}$', linewidth=1)
# plt.plot(x1, y1, '', linewidth=1, color="blue")
# plt.plot(x2, y2, '', linewidth=1, color="red")
plt.plot(x1, y1, '.', ms=5, color="orange")  # without IMBH
plt.plot(x2, y2, '.', ms=5, color="black")   # with IMBH
plt.legend(bbox_to_anchor=(0.77, 0.95), loc=2, borderaxespad=0., prop={'size': 6})


plt.ylabel('$\sigma$ [km/s]')
plt.xlabel('R [parsecs]')
ax.get_yaxis().set_tick_params(which='both', direction='in')
ax.get_xaxis().set_tick_params(which='both', direction='in')
ax.tick_params(axis='both', which='minor', bottom='on', top="on", right='on')

plt.draw()

# plt.figure(2)
#
# ax = plt.axes(xscale='', yscale='')
# plt.plot(x1, y1, '.', ms=5, color="orange")  # without IMBH
# plt.plot(x2, y2, '.', ms=5, color="black")   # with IMBH
#
#
# plt.ylabel('$\sigma$ [km/s]')
# plt.xlabel('R [parsecs]')
# ax.get_yaxis().set_tick_params(which='both', direction='in')
# ax.get_xaxis().set_tick_params(which='both', direction='in')
# ax.yaxis.set_minor_locator(AutoMinorLocator(4))
# ax2 = plt.twinx()
# ax2.get_xaxis().set_tick_params(which='both', direction='in')
# ax2.get_yaxis().set_tick_params(which='both', direction='in')
# ax2.yaxis.set_minor_locator(AutoMinorLocator(4))
# ax2.set_yticklabels([])
# ax.tick_params(axis='both', which='minor', bottom='on', top="on")
# plt.draw()

timeaveragedke1 = np.sum(ke1)/Variables[4]
timeaveragedpe1 = np.sum(pe1)/Variables[4]

timeaveragedke2 = np.sum(ke2)/Variables[4]
timeaveragedpe2 = np.sum(pe2)/Variables[4]


virial = timeaveragedke1 + timeaveragedpe1
virial2 = timeaveragedke2 + timeaveragedpe2

fig = plt.figure(3)  # Energy Diagrams without
ax10 = plt.axes(xscale='', yscale='')
ax10.get_xaxis().set_tick_params(which='both', direction='in')
ax10.get_yaxis().set_tick_params(which='both', direction='in')
ax10.tick_params(axis='both', which='minor', bottom='on', top="on")
plt.plot(time, ke1, '-', color="red", label="KE")
plt.plot(time, pe1, color="blue", label="PE")
plt.plot(time, ke1+pe1, color="darkblue", label="Total - No IMBH")
# plt.plot(time, [virial2]*Variables[4], '--', color="black")
plt.xlabel('Age (million years)')
plt.ylabel('Energy (joules)')
plt.legend(bbox_to_anchor=(0.77, 0.95), loc=2, borderaxespad=0., prop={'size': 6})


plt.figure(4)  # Energy Diagrams with IMBH
# plt.plot(time, ke2, color="Red", label="ke")
# plt.plot(time, pe2, color="Blue", label="PE")
plt.plot(time, np.zeros(len(time)), '--', color="blue")
plt.plot(time, ((ke2+pe2))/max(((ke2+pe2))*10), color="red", label="Total - IMBH")
plt.plot(time, ((ke1+pe1))/max(((ke1+pe1))*10), color="darkblue", label="Total - IMBH")
plt.ylabel('Energy Variation')
plt.xlabel('Age (million years)')
print (sum(ke1) + sum(pe1))/2000
print (sum(ke2) + sum(pe2))/2000
plt.figure(5)
ax9 = plt.axes(xscale='', yscale='')
plt.plot(time2, SMBHr, color="coral", label='No IMBH R$_{RMS}$')
# plt.plot(time2, .., '--', color="coral", label='IMBH $1000M_{\odot}$ R$_{RMS}$')
plt.xlabel('Age (million years)')
plt.ylabel('R$_{RMS}$ (parsecs)')

plt.legend(bbox_to_anchor=(0.70, 0.2), loc=2, borderaxespad=0., prop={'size': 6})

ax8 = ax9.twinx()  # instantiate a second axes that shares the same x-axis
# ax8.plot(time, RMSVr1, color="green", label='No IMBH V$_{RMS}$ ')
ax8.plot(time2, SMBHv, '--', color="darkgreen", label='IMBH $1000M_{\odot}$ V$_{RMS}$')
ax8.set_ylabel('V$_{RMS}$ (km/s)')


plt.legend(bbox_to_anchor=(0.7, 0.1), loc=2, borderaxespad=0., prop={'size': 6})

plt.show()

kehistory1 = np.zeros(1000)
pehistory1 = np.zeros(1000)
kehistory2 = np.zeros(1000)
pehistory2 = np.zeros(1000)
for i in range(1000):
    kehistory1[i] = ke1[i+1000]
    pehistory1[i] = pe1[i+1000]
    kehistory2[i] = ke2[i + 1000]
    pehistory2[i] = pe2[i + 1000]

v1 = 2*sum(kehistory1) + sum(pehistory1)
v2 = 2*sum(kehistory2) + sum(pehistory2)

print 2*v1/Variables[4], 2*v2/Variables[4]