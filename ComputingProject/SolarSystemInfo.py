
"""A file storing the solar system Information"""


solarmass = 1.9889*(10**30)      # Kilograms

earthmass = 5.972*(10**24)      # Kilograms
earthradius = 149.6*(10**6)     # Kilometeres
earthperiod = 365.256           # Days

jupitermass = 1.89813*(10**27)  # Kilograms
jupiterradius = -778.54*(10**6)  # Kilometeres
jupiterperiod = 4332.589        # Days

marsmass = 0.64171*(10**24)
marsradius = -227.92*(10**6)
marsperiod = 686.980

"""Orbital conditions, ie sun, earth, jupiter + .... ?"""
Orbitconditions = [
    [solarmass, 0, 0],
    [earthmass, earthradius, earthperiod],
    [jupitermass, jupiterradius, jupiterperiod],
    [marsmass, marsradius, marsperiod]
    ]