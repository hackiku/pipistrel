import sys
import streamlit as st
sys.path.append('./pages')
from draw_hifi import Line, calculate_pixel_length, convert_px_to_m


def calculate_error(real_value, calculated_value):
    """Calculate the percentage error."""
    return abs(real_value - calculated_value) / real_value * 100

def main():
    # Dictionary to store your measurements
    measurements = {
        'Wing Measurement': {'real_length': 4.855, 'pixel_length': None, 'calculated_length': None},
        'Tail Measurement': {'real_length': 3.210, 'pixel_length': None, 'calculated_length': None},
        # Add other measurements
    }

    # Calculate pixel lengths using functions from draw_hifi.py
    for key in measurements:
        line = Line()  # Modify as needed based on how you initialize Line in draw_hifi.py
        measurements[key]['pixel_length'] = calculate_pixel_length(line)

    # Calculate conversion factor
    conversion_factor = convert_px_to_m(measurements)

    # Calculate and store calculated lengths
    for key, values in measurements.items():
        pixel_length = values['pixel_length']
        measurements[key]['calculated_length'] = pixel_length * conversion_factor if conversion_factor else None

    # Calculate and display errors
    print("\nMeasurement Errors:")
    for key, values in measurements.items():
        error = calculate_error(values['real_length'], values['calculated_length'])
        print(f"{key}: Error = {error:.2f}%")

if __name__ == "__main__":
    main()