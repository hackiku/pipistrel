import math

# Standard sea level pressure, temperature and air density:
T0 = 288.15     # [K]
p0 = 101325.0   # [Pa]
rho0 = 1.225    # [kg/m^3]

# Standard acceleration due to gravity:
g = 9.80665     # [kg*m/s^2]

# Specific gas constant for air:
R = 287.058     # [J/(kg*K)]

# Lapse rates and atmospheric zones altitudes:
h_ts, a_ts = 0, -0.0065  # Troposphere
h_tp, a_tp = 11000, 0    # Tropopause
h_ss1, a_ss1 = 20000, 0.001  # Stratosphere (1)
h_ss2, a_ss2 = 32000, 0.0028  # Stratosphere (2)
h_sp, a_sp = 47000, 0    # Stratopause
h_ms1, a_ms1 = 51000, -0.0028  # Mesosphere (1)
h_ms2, a_ms2 = 71000, -0.002  # Mesosphere (2)
h_fin = 85000   # Final altitude considered

def get_parameters(altitude):
    altitude = altitude * 1000  # Convert altitude from [km] to [m]

    # Upper boundary of troposphere
    T_1 = T0 + a_ts * (h_tp - h_ts)
    p_1 = p0 * (T_1/T0)**(-g/(a_ts*R))
    rho_1 = rho0 * (T_1/T0)**(-g/(a_ts*R) - 1)

    # Upper boundary of tropopause
    T_2 = T_1
    p_2 = p_1 * math.exp(-(g/(R*T_2)) * (h_ss1 - h_tp))
    rho_2 = rho_1 * math.exp(-(g/(R*T_2)) * (h_ss1 - h_tp))

    # Upper boundary of stratosphere (1)
    T_3 = T_2 + a_ss1 * (h_ss2 - h_ss1)
    p_3 = p_2 * (T_3/T_2)**(-g/(a_ss1*R))
    rho_3 = rho_2 * (T_3/T_2)**(-g/(a_ss1*R) - 1)

    # Upper boundary of stratosphere (2)
    T_4 = T_3 + a_ss2 * (h_sp - h_ss2)
    p_4 = p_3 * (T_4/T_3)**(-g/(a_ss2*R))
    rho_4 = rho_3 * (T_4/T_3)**(-g/(a_ss2*R) - 1)

    # Upper boundary of stratopause
    T_5 = T_4
    p_5 = p_4 * math.exp(-(g/(R*T_5)) * (h_ms1 - h_sp))
    rho_5 = rho_4 * math.exp(-(g/(R*T_5)) * (h_ms1 - h_sp))

    # Upper boundary of mesosphere (1)
    T_6 = T_5 + a_ms1 * (h_ms2 - h_ms1)
    p_6 = p_5 * (T_6/T_5)**(-g/(a_ms1*R))
    rho_6 = rho_5 * (T_6/T_5)**(-g/(a_ms1*R) - 1)

    # Determine the zone and perform calculations
    if altitude < h_tp:
        zone = 'Troposphere'
        T_fin = T0 + a_ts * (altitude - h_ts)
        p_fin = p0 * (T_fin/T0)**(-g/(a_ts*R))
        rho_fin = rho0 * (T_fin/T0)**(-g/(a_ts*R) - 1)
    elif altitude < h_ss1:
        zone = 'Tropopause'
        T_fin = T_1
        p_fin = p_1 * math.exp(-(g/(R*T_fin)) * (altitude - h_tp))
        rho_fin = rho_1 * math.exp(-(g/(R*T_fin)) * (altitude - h_tp))
    elif altitude < h_ss2:
        zone = 'Stratosphere (1)'
        T_fin = T_2 + a_ss1 * (altitude - h_ss1)
        p_fin = p_2 * (T_fin/T_2)**(-g/(a_ss1*R))
        rho_fin = rho_2 * (T_fin/T_2)**(-g/(a_ss1*R) - 1)
    elif altitude < h_sp:
        zone = 'Stratosphere (2)'
        T_fin = T_3 + a_ss2 * (altitude - h_ss2)
        p_fin = p_3 * (T_fin/T_3)**(-g/(a_ss2*R))
        rho_fin = rho_3 * (T_fin/T_3)**(-g/(a_ss2*R) - 1)
    elif altitude < h_ms1:
        zone = 'Stratopause'
        T_fin = T_4
        p_fin = p_4 * math.exp(-(g/(R*T_fin)) * (altitude - h_sp))
        rho_fin = rho_4 * math.exp(-(g/(R*T_fin)) * (altitude - h_sp))
    elif altitude < h_ms2:
        zone = 'Mesosphere (1)'
        T_fin = T_5 + a_ms1 * (altitude - h_ms1)
        p_fin = p_5 * (T_fin/T_5)**(-g/(a_ms1*R))
        rho_fin = rho_5 * (T_fin/T_5)**(-g/(a_ms1*R) - 1)
    else:
        zone = 'Mesosphere (2)'
        T_fin = T_6 + a_ms2 * (altitude - h_ms2)
        p_fin = p_6 * (T_fin/T_6)**(-g/(a_ms2*R))
        rho_fin = rho_6 * (T_fin/T_6)**(-g/(a_ms2*R) - 1)

    return T_fin, p_fin, rho_fin, zone

def get_ISA_conditions(altitude):

    # Troposphere (0-10,999)m
    # Tropopause (11-19,999)m
    # Stratosphere (20-31,999)m
    # Stratosphere (32-46,999)m
    # Stratopause (47-50,999)m
    # Mesosphere (51-70,999)m
    # Mesosphere (71-85,000)m

    def speed_of_sound(temperature):
        gamma = 1.4  # Ratio of specific heats for air
        return math.sqrt(gamma * R * temperature)

    temperature, pressure, density, zone = get_parameters(altitude / 1000)  # Convert m to km
    sound_speed = speed_of_sound(temperature)
    return temperature, pressure, density, sound_speed, zone
