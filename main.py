import streamlit as st
import pandas as pd
from virus_model_streamlit.virus_viewer_component import virus_viewer
import inspect
from calcs import *
from data import aircraft_specs
import streamlit.components.v1 as components

def create_specs_table(aircraft_specs):
    specs_data = []
    for category, data in aircraft_specs.items():
        # Add a category header as a separate entry
        specs_data.append({
            "Specification": f"**{category}**",  # Mark category names distinctly
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

def spacer(height='5em'):
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align: center;'>Aerodynamics & Airfoils</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Pipistrel Virus SW 121</h5>", unsafe_allow_html=True)
    spacer("5em")

    # 3D model
    svelte_app_url = "https://pipewriter.vercel.app/pipistrel"
    components.iframe(svelte_app_url, width=700, height=500)

    # specs table
    all_specs_df = create_specs_table(aircraft_specs)
    preset = st.selectbox("Select Preset", ["Airfoil", "All"], index=0)
    filtered_df = filter_data_for_preset(all_specs_df, preset)
    st.table(filtered_df)  # Display the table


    # specs
    
     
    

    col1, col2 = st.columns(2)
    with col1:
        st.header("Aircraft Specifications")
    with col2:
        unit_system = st.radio("Select Unit System", ('SI Units', 'Aviation Units'))

    st.markdown('***')

    st.header("Airframe Choice")
    st.write("Calculating the computational wing area")

    st.image("./assets/side_front.png")
    st.image("./assets/wing.png")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Wing Area")
        st.latex(r"S_0 = \frac{l_0 + l_1}{2} \cdot \frac{b}{2}")
        st.latex(r"= \frac{1.576 + 3.028}{2} \cdot \frac{4.475}{2}")
        st.latex(r"S_0 = 10.301 \, \text{m}^2")
    with col2:
        wing_area_code = inspect.getsource(calculate_wing_surface_area)
        st.code(wing_area_code, language='python')
    
    st.markdown('<div style="margin: 5em;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Average mass of aircraft")
    with col2:
        average_mass_code = inspect.getsource(calculate_average_mass)
        st.code(average_mass_code, language='python')
    st.latex(r"m_r = \frac{m_{max} + m_{min}}{2} = \frac{6700 + 12500}{2} = 9600 \, \text{kg}")
    
    # calcs

    st.markdown('***')

    st.subheader("ISA air conditions")
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
    with st.echo():
        import math
        print('camadonna')
        st.write("This code block is being displayed and executed.")

    spacer('3em')

    st.markdown('***')
        

    
if __name__ == "__main__":
    main()