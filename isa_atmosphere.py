# isa_atmosphere.py 

''' ------------------------------------------------------------------
This module defines the Standard Atmosphere.

The function `get_parameters` takes the input altitude in [km]
and computes temperature, pressure and density at that altitude.

Data was taken from:

https://en.wikipedia.org/wiki/Standard_sea_level
https://en.wikipedia.org/wiki/Standard_gravity
https://en.wikipedia.org/wiki/Gas_constant
https://en.wikipedia.org/wiki/International_Standard_Atmosphere
------------------------------------------------------------------ '''

import numpy as np

# Standard sea level pressure, temperature and air density:
T0 = 288.15     # [K]
p0 = 101325.0   # [Pa]
rho0 = 1.225    # [kg/m3]

# Standard acceleration due to gravity:
g = 9.80665     # [kg*m/s2]

# Specific gas constant for air:
R = 287.058     # [J/(kg*K)]

# Lapse rates and atmospheric zones altitudes:
# TROPOSPHERE .......................................... (0-10.999)km
h_ts = 0        # [m]
a_ts = -0.0065  # [K/m]
# TROPOPAUSE ========================================== (11-19.999)km
h_tp = 11000    # [m]
a_tp = 0        # [K/m] (isothermal)
# STRATOSPHERE ........................................ (20-31.999)km
h_ss1 = 20000   # [m]
a_ss1 = 0.001   # [K/m]
# ..................................................... (32-46.999)km
h_ss2 = 32000   # [m]
a_ss2 = 0.0028  # [K/m]
# STRATOPAUSE ========================================= (47-50.999)km
h_sp = 47000    # [m]
a_sp = 0        # [K/m] (isothermal)
# MESOSPHERE .......................................... (51-70.999)km
h_ms1 = 51000   # [m]
a_ms1 = -0.0028 # [K/m]
# ......................................................... (71-85)km
h_ms2 = 71000   # [m]
a_ms2 = -0.002  # [K/m]
# ===================================================================
h_fin = 85000   # [m]

def get_parameters(altitude):

    # Convert altitude from [km] to [m]:
    altitude = altitude * 1000

    # Temperature, pressure and density at the upper boundaries:
    # Upper boundary of troposphere: ....................................
    T_1 = T0 + a_ts * (h_tp - h_ts)
    p_1 = p0*(T_1/T0)**(-g/(a_ts*R))
    rho_1 = rho0*(T_1/T0)**(-g/(a_ts*R) - 1)

    # Upper boundary of tropopause: .....................................
    T_2 = T_1
    p_2 = p_1 * np.exp(-(g/(R*T_2)) * (h_ss1 - h_tp))
    rho_2 = rho_1 * np.exp(-(g/(R*T_2)) * (h_ss1 - h_tp))

    # Upper boundary of stratosphere (1): ...............................
    T_3 = T_2 + a_ss1 * (h_ss2 - h_ss1)
    p_3 = p_2*(T_3/T_2)**(-g/(a_ss1*R))
    rho_3 = rho_2*(T_3/T_2)**(-g/(a_ss1*R) - 1)

    # Upper boundary of stratosphere (2): ...............................
    T_4 = T_3 + a_ss2 * (h_sp - h_ss2)
    p_4 = p_3*(T_4/T_3)**(-g/(a_ss2*R))
    rho_4 = rho_3*(T_4/T_3)**(-g/(a_ss2*R) - 1)

    # Upper boundary of stratopause: ....................................
    T_5 = T_4
    p_5 = p_4 * np.exp(-(g/(R*T_5)) * (h_ms1 - h_sp))
    rho_5 = rho_4 * np.exp(-(g/(R*T_5)) * (h_ms1 - h_sp))

    # Upper boundary of mezosphere (1): .................................
    T_6 = T_5 + a_ms1 * (h_ms2 - h_ms1)
    p_6 = p_5*(T_6/T_5)**(-g/(a_ms1*R))
    rho_6 = rho_5*(T_6/T_5)**(-g/(a_ms1*R) - 1)

    # Upper boundary of mezosphere (2): .................................
    T_7 = T_6 + a_ms2 * (h_fin - h_ms2)

    # Temperature, pressure and density calculation:
    if altitude >= h_ts and altitude < h_tp:
        print('You are in the troposphere.')
        zone = 'troposphere'
        # In the troposphere:
        T_fin = T0 + a_ts * (altitude - h_ts)
        p_fin = p0*(T_fin/T0)**(-g/(a_ts*R))
        rho_fin = rho0*(T_fin/T0)**(-g/(a_ts*R) - 1)

    elif altitude >= h_tp and altitude < h_ss1:
        print('You are in the tropopause.')
        print('Temperature is constant in this zone.')
        zone = 'tropopause'
        # In the tropopause:
        T_fin = T_1
        p_fin = p_1 * np.exp(-(g/(R*T_fin)) * (altitude - h_tp))
        rho_fin = rho_1 * np.exp(-(g/(R*T_fin)) * (altitude - h_tp))

    elif altitude >= h_ss1 and altitude < h_ss2:
        print('You are in the stratosphere (1).')
        zone = 'stratosphere (1)'
        # In the stratosphere (1):
        T_fin = T_2 + a_ss1 * (altitude - h_ss1)
        p_fin = p_2*(T_fin/T_2)**(-g/(a_ss1*R))
        rho_fin = rho_2*(T_fin/T_2)**(-g/(a_ss1*R) - 1)

    elif altitude >= h_ss2 and altitude < h_sp:
        print('You are in the stratosphere (2).')
        zone = 'stratosphere (2)'
        # In the stratosphere (2):
        T_fin = T_3 + a_ss2 * (altitude - h_ss2)
        p_fin = p_3*(T_fin/T_3)**(-g/(a_ss2*R))
        rho_fin = rho_3*(T_fin/T_3)**(-g/(a_ss2*R) - 1)

    elif altitude >= h_sp and altitude < h_ms1:
        print('You are in the stratopause.')
        print('Temperature is constant in this zone.')
        zone = 'stratopause'
        # In the stratopause:
        T_fin = T_4
        p_fin = p_4 * np.exp(-(g/(R*T_fin)) * (altitude - h_sp))
        rho_fin = rho_4 * np.exp(-(g/(R*T_fin)) * (altitude - h_sp))

    elif altitude >= h_ms1 and altitude < h_ms2:
        print('You are in the mezosphere (1).')
        zone = 'mezosphere (1)'
        # In the mezosphere (1):
        T_fin = T_5 + a_ms1 * (altitude - h_ms1)
        p_fin = p_5*(T_fin/T_5)**(-g/(a_ms1*R))
        rho_fin = rho_5*(T_fin/T_5)**(-g/(a_ms1*R) - 1)

    elif altitude >= h_ms2 and altitude <= h_fin:
        print('You are in the mezosphere (2).')
        zone = 'mezosphere (2)'
        # In the mezosphere (2):
        T_fin = T_6 + a_ms2 * (altitude - h_ms2)
        p_fin = p_6*(T_fin/T_6)**(-g/(a_ms2*R))
        rho_fin = rho_6*(T_fin/T_6)**(-g/(a_ms2*R) - 1)

    print("\nParameters at: " + str(altitude/1000) + " km:\n")
    print("Temperature: " + str(round(T_fin, 2)) + " K")
    print("Pressure: " + str(round(p_fin, 2)) + " Pa")
    print("Density: " + str(round(rho_fin, 5)) + " kg/m^3")

    print("\nPercentage of the sea level values:\n")
    print("Temperature: " + str(round(T_fin/T0*100, 2)) + "%")
    print("Pressure: " + str(round(p_fin/p0*100, 5)) + "%")
    print("Density: " + str(round(rho_fin/rho0*100, 5)) + "%")

    return(T_fin, p_fin, rho_fin)

# Function end

# Example usage:
if __name__ == "__main__":
    altitude = 10  # Example altitude in km
    temperature, pressure, density = get_parameters(altitude)
    print(f"At {altitude} km: Temperature = {temperature} K, Pressure = {pressure} Pa, Density = {density} kg/m^3")