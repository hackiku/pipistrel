import streamlit as st
import pandas as pd
import inspect
from calcs import *
from data import aircraft_specs
import streamlit.components.v1 as components

# grab specs from data.py
def create_specs_table(aircraft_specs):
    specs_data = []
    for category, data in aircraft_specs.items():
        # Add a category header as a separate entry
        specs_data.append({
            "Specification": f"**{category}**",
            "Value": "", 
            "Unit": "", 
            "LaTeX": ""
        })
        # Add individual specs
        for spec, details in data.items():
            specs_data.append({
                "Specification": spec, 
                "Value": details.get('value', ''), 
                "Unit": details.get('unit', ''),   
                "LaTeX": details.get('latex', '')  
            })
    
    df = pd.DataFrame(specs_data)
    return df

# use data points in calculations
def get_specific_data(df, category):
    category_data = df[df['Specification'] == f"**{category}**"]
    if not category_data.empty:
        start_index = category_data.index[0] + 1
        end_index = df[df['Specification'].str.startswith('**', na=False)].index
        end_index = end_index[end_index > start_index].min()

        return df[start_index:end_index]
    return pd.DataFrame()


# "Airfoil" preset manual filter
def filter_data_for_preset(data, preset):
    airfoil_columns = [
        'Length', 'Height', 'Wing Area', 'Aspect Ratio', 'Wingspan', 
        'Max Power', 'Never Exceed Speed', 'Max Structural Cruising Speed', 
        'Stall Speed Without Flaps', 'Best Climb Speed', 'Max Climb Rate', 'Maximum Operating Altitude'
    ]

    if preset == "Airfoil":
        # filtered_data = data[data['Specification'].isin(airfoil_columns)]
        filtered_data = pd.DataFrame([data.loc[data['Specification'] == spec].iloc[0] for spec in airfoil_columns if spec in data['Specification'].values])

    else:  # 'All' or any other preset
        filtered_data = data

    return filtered_data

# vertical whitespace
def spacer(height='5em'):
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

# airspeed
def main():
    st.markdown("<h1 style='text-align: center;'>Aircalcs</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Pipistrel Virus SW 121</h5>", unsafe_allow_html=True)
    spacer("5em")

    # 3D model
    svelte_app_url = "https://pipewriter.vercel.app/pipistrel"
    components.iframe(svelte_app_url, width=700, height=500)


    st.markdown('***')

    # 1. specs
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("1. Aircraft Specs")
    with col2:
        unit_system = st.radio("", ('SI Units', 'Aviation Units'))

    # specs table
    all_specs_df = create_specs_table(aircraft_specs)
    preset = st.selectbox("Select Preset", ["Airfoil", "All"], index=0)
    filtered_df = filter_data_for_preset(all_specs_df, preset)
    st.table(filtered_df)

    
    # 3col
    col1, col2, col3 = st.columns(3)
    with col1:
        l0 = st.number_input('Root Chord Length (l0) [m]', value=1.0, min_value=0.0, step=0.1)
    with col2:
        l1 = st.number_input('Tip Chord Length (l1) [m]', value=1.0, min_value=0.0, step=0.1)
    with col3:
        b = st.number_input('Wingspan (b) [m]', value=1.0, min_value=0.0, step=0.1)

    st.markdown('***')

    # ====================

    st.title("2. Airfoil selection")
    spacer('2em')
    
    # 2.1. wing area

    st.subheader('2.1. Wing area calculator')
    st.write("At early design stages we approximate the area geometrically to kickstart the airfoil selection process.")
    
    st.image('./assets/wing_black.jpg')
    
    # select l0, l1, b
    col1, col2 = st.columns(2)
    with col1:
        l0 = st.number_input('l0 - Root Chord Length (m)', value=1.576, min_value=0.0, step=0.1)
        l1 = st.number_input('Tip Chord Length (l1) [m]', value=3.028, min_value=0.0, step=0.1)
        b = st.number_input('Wingspan (b) [m]', value=4.475, min_value=1.0, step=0.1)
        col11, col12 = st.columns(2)
        with col11:
            if st.button('Calculate Wing Area'):
                wing_area = 0.5 * b * (l0 + l1)
                st.write(f"The calculated wing area is: {wing_area:.2f} square meters")
        with col12:
            if st.button('🔄 Reset'):
                # Reset logic goes here
                pass
    with col2:
        wing_area_code = inspect.getsource(calculate_wing_surface_area)
        st.code(wing_area_code, language='python')

    st.latex(r"""
    S_0 = (\frac{l_0 + l_1}{2} \cdot \frac{b}{2}) = \frac{1.576 + 3.028}{2} \cdot \frac{4.475}{2} = 10.301 \, \text{m}^2
    """)
    st.latex("S = 20.602 \ {m}^2")
        
    spacer('2em')
    
# ====================

    st.header('2.2. Average mass')

    # Extracting weight data
    weights_data_df = get_specific_data(all_specs_df, "Weights")

    # Filter to include only specific entries
    required_specs = ["Design Empty Weight", "Max Take Off Weight"]
    filtered_weights_df = weights_data_df[weights_data_df['Specification'].isin(required_specs)]

    # Create input fields for selected weight specifications
    col1, col2 = st.columns(2)
    with col1:

        design_empty_weight = max_take_off_weight = 0.0

        # Iterate through filtered weights data and create input fields
        for index, row in filtered_weights_df.iterrows():
            default_value = float(row['Value'])
            spec = row['Specification']
            description = row['Unit']

            if spec == "Design Empty Weight":
                design_empty_weight = st.number_input(
                    label=f"{spec} ({description})", 
                    value=default_value, 
                    min_value=0.0, 
                    step=0.1,
                    format="%.2f"
                )
            elif spec == "Max Take Off Weight":
                max_take_off_weight = st.number_input(
                    label=f"{spec} ({description})", 
                    value=default_value, 
                    min_value=0.0, 
                    step=0.1,
                    format="%.2f"
                )

    # Button to calculate average mass
    if st.button('Calculate Average Mass'):
        average_mass = calculate_average_mass(max_take_off_weight, design_empty_weight)
        # Format average_mass to 2 decimal places
        average_mass_formatted = f"{average_mass:.2f}"
        st.latex(fr"m_r = \frac{{m_{{max}} + m_{{min}}}}{2} = \frac{{{max_take_off_weight:.2f} + {design_empty_weight:.2f}}}{2} = {average_mass_formatted} \, \text{{kg}}")
    else:
        st.latex(r"m_r = \frac{m_{max} + m_{min}}{2}")

    with col2:
        average_mass_code = inspect.getsource(calculate_average_mass)
        st.code(average_mass_code, language='python')
    

    spacer('2em')

# ====================


    # 2.3 ISA conditions

    st.header("ISA air conditions")
    col1, col2 = st.columns(2)
    with col1:
        
        col11, col12 = st.columns([3,1])
        with col11:
            altitude_input = st.number_input("Altitude (m)", value=3000)
        with col12:
            st.markdown('<div style="margin-top: 1.8em;"></div>', unsafe_allow_html=True)
            # st.button("Clear")
        st.latex(r"T = 255.65 \, \text{K} \, (T = -17.5 \, \text{°C})")
        st.latex(r"P = 54019.9 \, \text{Pa}")
        st.latex(r"\rho = 0.736116 \, \text{kg/m}^3")
        st.latex(r"c = 320.529 \, \text{m/s}")
    with col2:
        isa_conditions_code = inspect.getsource(get_ISA_conditions)
        st.code(isa_conditions_code, language='python')

# ====================

    spacer('3em')

    st.subheader("Cruise speed")
    col1, col2 = st.columns(2)
    with col1:
        st.latex(r"v_{krst} = M_{krst} \cdot c")
        st.latex(r"= 0.7 \cdot 320.529")
        st.latex(r"v_{krst} = 224.37 \, \text{m/s} \, (807.73 \, \text{km/h})")
    with col2:
        cruise_speed_code = inspect.getsource(calculate_cruise_speed)
        st.code(cruise_speed_code, language='python')

    spacer('3em')

    st.subheader("Drag Coefficient")
    st.write("Enter the following parameters to calculate the drag coefficient during cruise flight:")
    
    col1, col2 = st.columns(2)
    with col1:
        mr_input = st.number_input("Average Aircraft Mass (mr) [kg]", value=9600.0)
        rho_input = st.number_input("Air Density (rho) [kg/m^3]", value=0.736116)
        v_cruise_input = st.number_input("Cruise Speed (v_cruise) [m/s]", value=224.37)
        S_input = st.number_input("Wing Reference Area (S) [m^2]", value=20.602)

        calculate_button, clear_button = st.columns([3, 1])
        with calculate_button:
            if st.button('Calculate Drag Coefficient'):
                C_D_cruise = calculate_drag_coefficient(mr_input, rho_input, v_cruise_input, S_input)
                st.write(f"The calculated drag coefficient (C_D_cruise) is: {C_D_cruise:.3f}")
        with clear_button:
            if st.button('Clear'):
                clear_values()

    with col2:
        isa_conditions_code = inspect.getsource(get_ISA_conditions)
        st.code(isa_conditions_code, language='python')

    st.markdown('***')

            
if __name__ == "__main__":
    main()