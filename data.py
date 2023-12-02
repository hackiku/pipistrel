aircraft_specs = {
    "Model": {
        "Name": {"value": "VIRUS SW 121A – EXPLORER", "description": "Model name of the aircraft"},
        "Engine": {"value": "Rotax 912 S3", "description": "Type of engine used in the aircraft"},
        "Max Power": {
            "value": 73.5, "unit": "kW", 
            "value_alt": 100, "unit_alt": "hp", 
            "description": "Maximum power of the engine"
        },
        # ... other model data
    },
    "Dimensions": {
        "Length": {
            "value": 6.42, "unit": "m", 
            "value_alt": 21.06, "unit_alt": "ft", 
            "description": "Total length of the aircraft"
        },
        "Wingspan": {
            "value": 10.70, "unit": "m", 
            "value_alt": 35.10, "unit_alt": "ft", 
            "description": "Distance from one wingtip to the other"
        },
        "Height": {
            "value": 1.90, "unit": "m", 
            "value_alt": 6.23, "unit_alt": "ft", 
            "description": "Height of the aircraft"
        },
        "Wing Area": {
            "value": 9.51, "unit": "m²", 
            "value_alt": 102.4, "unit_alt": "ft²", 
            "description": "Total area of the wings"
        },
        "Mean Aerodynamic Chord": {
            "value": 0.898, "unit": "m", 
            "value_alt": 2.95, "unit_alt": "ft", 
            "description": "Average distance from the leading edge to the trailing edge of the wing"
        },
        "Aspect Ratio": {
            "value": 12.04, "unit": "", 
            "description": "Ratio of the wingspan to the mean chord"
        },
        # ... other dimensions
    },
    "Weights": {
        "Design Empty Weight": {
            "value": 371, "unit": "kg", 
            "value_alt": 818, "unit_alt": "lb", 
            "description": "Weight of the aircraft without payload or fuel"
        },
        "Max Take Off Weight": {
            "value": 600, "unit": "kg", 
            "value_alt": 1323, "unit_alt": "lb", 
            "description": "Maximum weight for takeoff"
        },
        "Design Useful Load": {
            "value": 229, "unit": "kg", 
            "value_alt": 505, "unit_alt": "lb", 
            "description": "Weight of passengers, cargo, and fuel the aircraft can carry"
        },
        "Max Baggage Weight": {
            "value": 25, "unit": "kg", 
            "value_alt": 55, "unit_alt": "lb", 
            "description": "Maximum weight of baggage"
        },
        # ... other weights
    },
    "Performance": {
        "Never Exceed Speed": {
            "value": 301.9, "unit": "km/h",  
            "value_alt": 163, "unit_alt": "KTAS",
            "description": "Maximum speed the aircraft should not exceed",
            "latex": "V_{ne}"
        },
        "Max Structural Cruising Speed": {
            "value": 222.2, "unit": "km/h",  
            "value_alt": 120, "unit_alt": "KIAS",
            "description": "Maximum cruising speed except in smooth air",
            "latex": "V_{no}"
        },
        "Max Operating Manoeuvring Speed": {
            "value": 185.2, "unit": "km/h",  
            "value_alt": 100, "unit_alt": "KIAS",
            "description": "Maximum speed for safe maneuvering",
            "latex": "V_{a}"
        },
        "Max Flaps Extended Speed": {
            "value": 149.7, "unit": "km/h",  
            "value_alt": 81, "unit_alt": "KIAS",
            "description": "Maximum speed with flaps extended",
            "latex": "V_{fe}"
        },
        "Max Airbrakes Extended Speed": {
            "value": 185.2, "unit": "km/h",  
            "value_alt": 100, "unit_alt": "KIAS",
            "description": "Maximum speed with airbrakes extended",
            "latex": "V_{ae}"
        },
        "Stall Speed With Flaps": {
            "value": 87, "unit": "km/h",  
            "value_alt": 47, "unit_alt": "KIAS",
            "description": "Stall speed with flaps extended",
            "latex": "V_{s0}"
        },
        "Stall Speed Without Flaps": {
            "value": 98.2, "unit": "km/h",  
            "value_alt": 53, "unit_alt": "KIAS",
            "description": "Stall speed without flaps",
            "latex": "V_{s}"
        },
        "Best Climb Speed": {
            "value": 144.8, "unit": "km/h",  
            "value_alt": 78, "unit_alt": "KIAS",
            "description": "Optimal speed for maximum climb rate",
            "latex": "V_{y}"
        },
        "Max Climb Rate": {
            "value": 5.33, "unit": "m/s",
            "value_alt": 1050, "unit_alt": "ft/min",
            "description": "Maximum rate at which the aircraft can climb",
            "latex": "R_{climb}"
        },
        "Take Off Distance at SL": {
            "value": 160, "unit": "m",
            "value_alt": 525, "unit_alt": "ft",
            "description": "Distance required for takeoff at sea level",
            "latex": "D_{to, SL}"
        },
        "Maximum Take-Off Altitude": {
            "value": 3048, "unit": "m",
            "value_alt": 10000, "unit_alt": "ft",
            "description": "Maximum altitude for take-off",
            "latex": "H_{max, TO}"
        },
        "Maximum Operating Altitude": {
            "value": 5486, "unit": "m",
            "value_alt": 18000, "unit_alt": "ft",
            "description": "Maximum altitude for aircraft operation",
            "latex": "H_{max, op}"
        },
        "Permitted Fuel": {
            "value": "AVGAS, MOGAS, or car fuel (min RON 95; EN228 Premium or Premium plus with max. 10% Ethanol)",
            "description": "Types of fuel that can be used",
            "latex": "F_{type}"
        },
        "Fuel Consumption at 2000 ft. 75% Power": {
            "value": 18.4, "unit": "l/h",
            "value_alt": 4.86, "unit_alt": "gal/h",
            "description": "Fuel consumption at 2000 feet with 75% power",
            "latex": "FC_{2000ft, 75%}"
        },
        "Endurance at 4000 ft., 65% Power": {
            "value": "5 h 33 min", "unit": "",
            "description": "Endurance time at 4000 feet with 65% power, plus 30 min reserve",
            "latex": "E_{4000ft, 65%}"
        },
        "Range Distance at 4000 ft., 65% Power": {
            "value": 1189, "unit": "km",
            "value_alt": 642, "unit_alt": "nmi",
            "description": "Range distance at 4000 feet with 65% power, plus 30 min reserve",
            "latex": "R_{4000ft, 65%}"
        },
        "Noise Level": {
            "value": 70, "unit": "dB(A)",
            "description": "Noise level as measured by ICAO Annex 16, Chapter 10",
            "latex": "NL_{ICAO}"
        },
        "Flight Load Factor Limits": {
            "value": "+4.0 g / -2.0 g",
            "description": "Operational load factor limits for the aircraft",
            "latex": "LF_{limits}"
        },
        # ... any additional performance data
    },
    # ... other categories
}
