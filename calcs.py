# calcs.py

aircraft_specs = {
    "Dimensions": {
        "Length": 13.23,
        "Wingspan": 8.95,
        "Height": 4.55,
        "Wing Area": 20.6
    },
    "Mass": {
        "Empty": 6700,
        "Maximum Takeoff": 13000
    },
    "Propulsion": {
        "Engine": "Rolls-Royce Spey 807 turbofan",
        "Thrust": 49.1
    },
    "Performance": {
        "Maximum Speed": 1053,
        "Cruise Speed": 807.73,
        "Climb Rate": 52.1,
        "Combat Radius": 889
    }
}

# Define the units separately
units_si = {
    "Dimensions": {
        "Length": "m",
        "Wingspan": "m",
        "Height": "m",
        "Wing Area": "m²"
    },
    "Mass": {
        "Empty": "kg",
        "Maximum Takeoff": "kg"
    },
    "Propulsion": {
        "Thrust": "kN"
    },
    "Performance": {
        "Maximum Speed": "km/h",
        "Cruise Speed": "km/h",
        "Climb Rate": "m/s",
        "Combat Radius": "km"
    }
}

# Example conversion function (to be expanded as needed)
def convert_units(specs, units, target_unit_system):
    # Conversion logic here...
    # Return converted specifications based on the target unit system
    return converted_specs

# Other functions can be added as needed...