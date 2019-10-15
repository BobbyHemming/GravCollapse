

# !!! To select which situation: !!!
select = 1

# !!! Cluster details: !!!
clusternumber = 50
numberofsteps = 2000

Radius = 3*(10**14)        # Cluster Radius [km]
epsilon = 0.1*Radius           # Softening Radius

NumberOfVariables = 3      # r,v,a - this is number of variables
G = 4.982174196*10**(-10)  # Gravitational Constant [km/d/kg]

v1 = 0.0
v2 = 10**4             # km/day
meanspeed = v1         # Mean Velocity in cluster
timestep = 1           # Leapfrog step in days - now just a placeholder

if select == 1:              # Cluster, random, no black hole
    NumberOfParticles = clusternumber
    nsteps = numberofsteps
elif select == 2:
    NumberOfParticles = clusternumber
    nsteps = numberofsteps
else:                        # Solar system, 3 particles, 100 orbits
    NumberOfParticles = 3
    timestep = 1
    nsteps = 36500

Variables = [NumberOfParticles, NumberOfVariables, G, timestep, nsteps, epsilon, Radius, meanspeed, select]

