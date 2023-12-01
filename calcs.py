# calcs.py

# ISA constants
T = 288.15  # Temperature (K)
p = 101325  # pressure (Pa)
rho = 0.736116  # density kg/m^3
c = 340.29  # Speed of Sound in m/s
g = 9.81  # Gravity acceleration (m/s^2)

def calculate_wing_surface_area(l0, l1, b):
    """
    l0 -- Root chord length (m)
    l1 -- Tip chord length (m)
    b -- Wingspan (m)
    """
    S_20 = (l0 + l1) / 2 * b / 2
    S = 2 * S_20  # Total wing surface area (m^2)
    return S

def calculate_average_mass(m_max, m_min):
    # average mass (kg)
    m_r = (m_max + m_min) / 2
    return m_r

def get_ISA_conditions():
    # Return ISA conditions at cruise altitude
    conditions = {
        'Temperature (K)': 255.65,
        'Pressure (Pa)': 54019.9,
        'Density (kg/m^3)': 0.736116,
        'Speed of Sound (m/s)': 320.529
    }
    return conditions

# ... (rest of the calculations)


# ... (rest of the calculations)

def calculate_drag_coefficient(mr, rho, v_cruise, S):
    """
    Calculate the drag coefficient during cruise flight.

    :param mr: average aircraft mass (kg)
    :param rho: air density (kg/m^3)
    :param v_cruise: cruise speed (m/s)
    :param S: wing reference area (m^2)
    :return: drag coefficient
    """
    q = 0.5 * rho * v_cruise ** 2
    C_D_cruise = (2 * mr * g) / (q * S)
    return C_D_cruise

def calculate_cruise_speed(M_krst, c):
    """
    Calculate the cruise speed of the aircraft.
    
    Parameters:
    M_krst -- Cruise Mach number
    c -- Speed of sound at cruising altitude (m/s)
    
    Returns:
    The cruise speed in m/s and km/h.
    """
    v_krst = M_krst * c
    return v_krst



# ======================= #

def calculate_cruise_speed():
    vkrst = 7.0 * c
    return vkrst

def convert_units(specs, units, target_unit_system):
    return converted_specs

aircraft_specs = {
    "Dimensions": {
        "Length": {"value": 13.23, "unit": "m", "latex": "L"},
        "Wingspan": {"value": 8.95, "unit": "m", "latex": "W"},
        "Height": {"value": 4.55, "unit": "m", "latex": "H"},
        "Wing Area": {"value": 20.6, "unit": "m²", "latex": "S"}
    },
    "Mass": {
        "Empty": {"value": 6700, "unit": "kg", "latex": "M_{empty}"},
        "Maximum Takeoff": {"value": 13000, "unit": "kg", "latex": "M_{max}"},
    },
    "Propulsion": {
        "Engine": {"value": "Rolls-Royce Spey 807 turbofan", "unit": "", "latex": ""},
        "Thrust": {"value": 49.1, "unit": "kN", "latex": "T"}
    },
    "Performance": {
        "Maximum Speed": {"value": 1053, "unit": "km/h", "latex": "V_{max}"},
        "Cruise Speed": {"value": 807.73, "unit": "km/h", "latex": "V_{cruise}"},
        "Climb Rate": {"value": 52.1, "unit": "m/s", "latex": "R_{climb}"},
        "Combat Radius": {"value": 889, "unit": "km", "latex": "R_{combat}"}
    }
}