### app.py ###
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import inspect
from data import aircraft_specs, create_specs_table 
from utils import spacer
from modules.isa_lite import get_ISA_conditions
# from modules.draw.draw import draw
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables

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

# ============================================================
# ============================================================

def main():
    
    page_values = [
        'S', 'l0', 'l1', 'b', 'm_sr', 'v_krst', 'T', 'P', 'rho', 'c', 
        'g', 'Re', 'c_z_krst'
    ]
    
    initialize_session_state()


    st.markdown("<h1 style='text-align: center;'>AircraftDesign.app</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Pipistrel Virus SW 121</h5>", unsafe_allow_html=True)
    spacer("5em")

    # 3D model
    # svelte_app_url = "https://pipewriter.vercel.app/pipistrel"
    # components.iframe(svelte_app_url, width=400, height=400)

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

    st.markdown('***')

# ==================== IMAGE ====================#

    st.title("2. Airfoil selection")
    spacer('2em')
    
    # 2.1. wing area
    st.subheader('2.1. Wing area calculator')

    # S.value, l0.v alue, l1.value, b.value = draw_hifi.main()
    
    # Create a Variable instance for S using the returned value
    st.markdown('***')

        
#==================== MASS ====================#

    st.subheader('2.2. Average mass')

    max_take_off_weight = aircraft_specs["Weights"]["Max Take Off Weight"]["value"]
    design_empty_weight = aircraft_specs["Weights"]["Design Empty Weight"]["value"]

    # max takeoff weight & design empty weight
    col1, col2 = st.columns(2)
    with col1:
        max_take_off_weight = st.number_input("Max Take Off Weight (kg)", value=max_take_off_weight, min_value=0,
        step=20)
    with col2:
        design_empty_weight = st.number_input("Design Empty Weight (kg)", value=design_empty_weight, min_value=0, 
        step=20)

    # Calculate average mass
    m_sr = (max_take_off_weight + design_empty_weight) / 2
    st.latex(f"m_{{\\text{{sr}}}} = \\frac{{m_{{\\text{{max}}}} + m_{{\\text{{min}}}}}}{2} = \\frac{{{max_take_off_weight:.2f} + {design_empty_weight:.2f}}}{2} = {m_sr:.2f} \\, \\text{{kg}}")

    st.markdown('***')

# ==================== ISA ====================#

    # 2.3 ISA conditions (from isa_lite.py)
    st.subheader("2.3. ISA air conditions")

    col1, col2 = st.columns(2)
    with col1:
        H = st.slider("Altitude (m)", min_value=0, value=get_variable_value('H'), max_value=30000, step=100)
        T, P, rho, c, zone = get_ISA_conditions(H)
        # rho = density
        max_operating_altitude = aircraft_specs["Performance"]["Maximum Operating Altitude"]["value"]
        max_altitude_percentage = H / max_operating_altitude * 100
        if max_altitude_percentage <= 100:
            st.success(f"👍 {max_altitude_percentage:.2f}% max operating altitude ({format(max_operating_altitude, ',')} m)")
        else:
            st.error(f"⚠️ Above max operating altitude ({format(max_operating_altitude, ',')} m)")
        st.write("You are flying in the:")
        st.info(f"🌍 {zone}")

    with col2:
        # Displaying the values and zone using LaTeX
        st.latex(f"H = {H} \, \ {{m}} \, \ ({H * 3.28084:.0f} \, \ {{ft}})")
        st.latex(f"T = {T:.2f} \, \ {{K}} \, ({T - 273.15:.2f} \ {{°C}})")
        st.latex(f"P = {P:.2f} \, \ {{Pa}}")
        st.latex(f"\\rho = {rho:.5f} \, \ {{kg/m}}^3")
        st.latex(f"c = {c:.2f} \, \ {{m/s}}")

    spacer()
    st.write('Kinematic viscosity calculated with the Sutherland formula')
    nu = (1.458e-6 * T**1.5) / (T + 110.4) / rho
    st.latex(r'\nu = \frac{\mu}{\rho} = \frac{1.458 \times 10^{-6} \cdot T^{1.5}}{T + 110.4} \cdot \frac{1}{\rho}')
    st.latex(f'\\nu = {nu:.2e} \\, \\text{{m}}^2/\\text{{s}}')
    
    
    st.markdown('***')

# ==================== CRUISE SPEED ====================#
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader("2.3. Define cruise speed")
    with col2:
        st.write()
        # unit = st.radio("", ['Km/h', 'm/s'])
    
    st.write(r"Recommended: 70-80% of Vne for piston engines.")

    # Retrieve the Never Exceed Speed from aircraft_specs
    v_ne_poh = aircraft_specs["Performance"]["Never Exceed Speed"]["value"]

    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        percentage_of_vne = st.slider("Percentage of Vne (%)", min_value=0, max_value=100, value=70, step=1)
    with col2:
        unit = st.radio("", ['Km/h', 'm/s'])
    with col3:
        if unit == 'Km/h':
            v_ne = st.number_input("Never Exceed Speed (Km/h)", value=v_ne_poh, min_value=0.00, step=10.00)
            v_krst = percentage_of_vne / 100.0 * (v_ne / 3.6)  # Convert to m/s
        else:
            v_ne = st.number_input("Never Exceed Speed (m/s)", value=v_ne_poh / 3.6, min_value=0.00, step=1.00)
            v_krst = percentage_of_vne / 100.0 * v_ne  # Already in m/s

    st.latex(f"v_{{\\text{{krst}}}} = \\frac{{\\text{{Vne}} \\times {percentage_of_vne}\\%}}{{100}} = \\frac{{{v_ne:.3f} \\times {percentage_of_vne}}}{{100}}")
    st.latex(f"v_{{\\text{{krst}}}} = {v_krst*3.6:.2f} \\, \\text{{Km/h}} = {v_krst:.2f} \\, \\text{{m/s}}")

    st.markdown('***')


#==================== LIFT COEFF ====================#

    st.subheader("Lift coefficient at cruise conditions")

    with st.expander("Manually change all parameters to recalculate Cz_krst"):
        planet = st.radio("Select Planet", ['Earth', 'Mars'], index=1)
        col1, col2, col3 = st.columns(3)
        with col1:
            S = st.number_input(f'Wing area', value=get_variable_value('S'), step=0.1, format="%.2f")
        with col2:
            m_sr = st.number_input('Average mass (kg)', value=get_variable_value('m_sr'), step=100.0, format="%.2f")
            # m_sr = st.number_input(f'{m_sr.name} ({m_sr.unit})', value=m_sr.value, step=100.0, format="%.2f")
        with col3:
            v_krst = st.number_input('Mass at cruise (kg)', value=get_variable_value('v_krst'), step=100.0, format="%.2f")
            # v_krst.value = st.number_input(f'{v_krst.name} ({v_krst.unit})', value=v_krst.value, step=0.1, format="%.2f")
        spacer()

        col1, col2, col3 = st.columns(3)
        with col1:
            if planet == 'Earth':
                altitude = st.number_input("Altitude (m)", value=H, min_value=0, step=100)
                temperature, pressure, density, sound_speed, zone = get_ISA_conditions(altitude)
            else:
                # rho = 0.020
                g = st.number_input('Gravity', value=3.711, step=0.01, format="%.5f")
                spacer('1em')
                st.warning(f"🪐 Mars")
        with col2:
            g = st.number_input('Gravity', value=9.80665, step=0.01, format="%.5f")
        with col3:
            st.write('rho TODO')
            # rho = st.number_input(f'Density', value=rho.value, step=0.001, format="%.5f")

    c_z_krst = (m_sr * g) / (0.5 * rho * v_krst**2 * S)
    st.latex(r"C_{Z_{krst}} = \frac{G}{q \cdot S} = \frac{m_{sr} \cdot g}{0.5 \cdot \rho \cdot v_{krst}^2 \cdot S}")
    st.latex(f"C_{{Z_{{krst}}}} = \\frac{{ {m_sr:.2f} \\cdot {g:.2f} }}{{ 0.5 \\cdot {rho:.4f} \\cdot {v_krst:.2f}^2 \\cdot {S:.2f} }}")
    st.latex(f"C_{{Z_{{krst}}}} = {c_z_krst:.3f}")
    
    st.markdown('***')
    #==================== SESSION STATE ====================#

    update_variables(page_values, locals())
    log_changed_variables()

    
    if st.button("render latex and save pics"):
        st.write("WIP")

if __name__ == "__main__":
    main()