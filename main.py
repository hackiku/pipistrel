import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import inspect
from data import Variable, aircraft_specs, create_specs_table
from isa_lite import get_ISA_conditions
from utils import spacer, variables_two_columns
from pages import draw_hifi

m_sr = Variable("Average mass", 535.50, "m_{sr}", "kg")
v_krst = Variable("Cruising speed", 224.37, r"v_{krst}", "m/s")
c_z_krst = Variable("Cruise lift coefficient", 0.247, r"C_{z_{krst}}", "")
S = Variable("Wing area", 1.00, "S", "m^2")

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
    st.markdown("<h1 style='text-align: center;'>Aircalcs</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>Pipistrel Virus SW 121</h5>", unsafe_allow_html=True)
    spacer("5em")

    # 3D model
    svelte_app_url = "https://pipewriter.vercel.app/pipistrel"
    components.iframe(svelte_app_url, width=400, height=400)

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

    S_value = draw_hifi.main()

    # Create a Variable instance for S using the returned value
    S = Variable("Wing Area", S_value, "S", "m²")
    
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
    m_sr.value = float (max_take_off_weight + design_empty_weight) / 2
    st.latex(f"m_{{\\text{{pr}}}} = \\frac{{m_{{\\text{{max}}}} + m_{{\\text{{min}}}}}}{2} = \\frac{{{max_take_off_weight:.2f} + {design_empty_weight:.2f}}}{2} = {m_sr.value:.2f} \\, \\text{{kg}}")

    spacer('2em')
    
# ==================== ISA

    rho = Variable("Air density at cruise altitude", 0.736116, r"\rho", "kg/m^3")
    g = Variable("Gravity acceleration", 9.80665, "g", "m/s²")
    
    altitude = 4500

    # 2.3 ISA conditions
    st.subheader("2.3. ISA air conditions")
    col1, col2 = st.columns(2)
    with col1:
        # Altitude slider using session state
        altitude_input = st.slider(
            "Altitude (m)", 
            min_value=0,
            value = altitude,
            max_value=50000, 
            # value=st.session_state['altitude'], 
            step=100)
        altitude = altitude_input

        # get ISA conditions from isa_lite.py
        temperature, pressure, density, sound_speed, zone = get_ISA_conditions(altitude)
        rho.value = density

        # Displaying the values and zone using LaTeX
        st.latex(f"T = {temperature:.2f} \, \ {{K}} \, ({temperature - 273.15:.2f} \ {{°C}})")
        st.latex(f"P = {pressure:.2f} \, \ {{Pa}}")
        st.latex(f"\\rho = {density:.5f} \, \ {{kg/m}}^3")
        st.latex(f"c = {sound_speed:.2f} \, \ {{m/s}}")
        st.info(f"🌍 {zone}")
        
    with col2:
        # Displaying source code for ISA conditions calculation
        isa_conditions_code = inspect.getsource(get_ISA_conditions)
        st.code(isa_conditions_code, language='python')

    spacer()

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
            v_krst.value = percentage_of_vne / 100.0 * (v_ne / 3.6)  # Convert to m/s
        else:
            v_ne = st.number_input("Never Exceed Speed (m/s)", value=v_ne_poh / 3.6, min_value=0.00, step=1.00)
            v_krst.value = percentage_of_vne / 100.0 * v_ne  # Already in m/s

    st.latex(f"v_{{\\text{{krst}}}} = \\frac{{\\text{{Vne}} \\times {percentage_of_vne}\\%}}{{100}} = \\frac{{{v_ne:.3f} \\times {percentage_of_vne}}}{{100}}")
    st.latex(f"v_{{\\text{{krst}}}} = {v_krst.value*3.6:.2f} \\, \\text{{Km/h}} = {v_krst.value:.2f} \\, \\text{{m/s}}")

    spacer()

#==================== LIFT COEFF ====================#

    st.subheader("Lift coefficient at cruise (c_z_krst)")

    with st.expander("Change parameters (m_sr, g, rho, v_krst) or lift coefficient value"):
        def calculate_c_z_krst():
            c_z_krst.value = (m_sr.value * g.value) / (0.5 * rho.value * v_krst.value**2 * S.value)
            # LaTeX string with variables
            numbers = (
                f"\\frac{{ {m_sr.value:.2f} \\cdot {g.value:.2f} }}"
                f"{{0.5 \\cdot {rho.value:.6f} \\cdot {v_krst.value:.2f}^2 \\cdot {S.value:.2f} }}"
            )
            # Formula in LaTeX format
            c_z_krst.formula = f"\\frac{{G}}{{q \\cdot S}} = \\frac{{m_{{sr}} \\cdot g}}{{0.5 \\cdot \\rho \\cdot v_{{krst}}^2 \\cdot S}} \\\\ [2em] {c_z_krst.latex} = {numbers}"

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            m_sr.value = st.number_input(f'{m_sr.name} ({m_sr.unit})', value=m_sr.value, step=100.0, format="%.2f")
        with col2:
            g.value = st.number_input(f'{g.name} ({g.unit})', value=g.value, step=0.01, format="%.3f")
        with col3:
            rho.value = st.number_input(f'{rho.name} ({rho.unit})', value=rho.value, step=0.001, format="%.5f")
        with col4:
            v_krst.value = st.number_input(f'{v_krst.name} ({v_krst.unit})', value=v_krst.value, step=0.1, format="%.2f")

        calculate_c_z_krst()
    
    st.latex(f"""{c_z_krst.latex} = {c_z_krst.formula}""")
    st.latex(f"{c_z_krst.latex} = {c_z_krst.value:.3f}")
    # st.latex(f"{c_z_krst.latex} = {c_z_krst.value:3f}")

  
    st.markdown('***')

    st.header("Airfoil selection")
            
if __name__ == "__main__":
    main()