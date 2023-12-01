# calcs.py

# ISA atmosphere
T = 288.15  # Temperature (K)
p = 101325  # pressure (Pa)
rho = 0.736116  # density kg/m^3
c = 340.29  # Speed of Sound in m/s

def calculate_cruise_speed():
    vkrst = 7.0 * c
    return vkrst

def convert_units(specs, units, target_unit_system):
    # Conversion logic here...
    # Return converted specifications based on the target unit system
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