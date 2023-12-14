import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import inspect
# from calcs import *
from data import Variable, aircraft_specs, create_specs_table
from isa_lite import get_ISA_conditions
from utils import spacer, variables_two_columns
from pages import draw_hifi
# from pages.draw_hifi import *
# from pages.draw_hifi import main as draw_hifi_main

# section = st.sidebar.radio('Go to section', ['Introduction', 'Aircraft Specs', 'Airfoil Selection', 'ISA Conditions', 'Performance Metrics'])

# b = Variable("Wingspan", 8.942, "b", "m")
# b = Variable("Wingspan", aircraft_specs["Dimensions"]["Wingspan"]["value"], "b", aircraft_specs["Dimensions"]["Wingspan"]["unit"])
S = Variable("Wing Area", 20.602, "S", "m²")
rho = Variable("Air density at cruise altitude", 0.736116, r"\rho", "kg/m^3")
g = Variable("Gravity acceleration", 9.80665, "g", "m/s²")

m_sr = Variable("Average mass", 9600.00, "m_{sr}", "kg")
v_krst = Variable("Cruising speed", 224.37, r"v_{krst}", "m/s")
c_z_krst = Variable("Cruise lift coefficient", 0.247, r"C_{z_{krst}}", "")

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

# ====================

    st.title("2. Airfoil selection")
    spacer('2em')
    
    # 2.1. wing area

    st.subheader('2.1. Wing area calculator')
    st.write("At early design stages we approximate the area geometrically to kickstart the airfoil selection process.")
    
    # image 

    draw_hifi.main()

    st.markdown('***')


    l0_m = Variable("Root Chord Length", draw_hifi.trapezoid.l_0 * 0.0084, "l_0", "m")
    l1_m = Variable("Tip Chord Length", draw_hifi.trapezoid.l_1 * 0.0084, "l_1", "m")
    b_m = Variable("Wingspan", 10.70, "b", "m")
    
    # st.write(f"l1 is {l1_poh} l0 is {l0_poh}")
    col1, col2, col3 = st.columns(3)
    with col1:
        l0_m.value = st.number_input('Root Chord Length (l0_m) [m]', value=l0_m.value, step=0.5)
    with col2:
        l1_m.value = st.number_input('Tip Chord Length (l1_m) [m]', value=l1_m.value, step=0.5)
    with col3:
        b_m.value = st.number_input('Wingspan (b) [m]', value=b_m.value, step=0.5)

    wing_area = 0.5 * b_m.value * (l0_m.value + l1_m.value)

    # wing surface formula
    st.latex(f"S = \\frac{{{l0_m.latex} + {l1_m.latex}}}{2} \\cdot {b_m.latex}")
    st.latex(f"S = \\frac{{{l0_m.value:.3f} + {l1_m.value:.3f}}}{2} \\cdot {b_m.value:.3f}")
    st.latex(f"S = {wing_area:.3f} \\, \\text{{m}}^2")
        
    spacer()
    
# ==================== MASS

    st.subheader('2.2. Average mass')

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
    if 'altitude' not in st.session_state:
        st.session_state['altitude'] = 5000  # Default altitude

    # 2.3 ISA conditions
    st.subheader("2.3. ISA air conditions")
    col1, col2 = st.columns(2)
    with col1:
        # Altitude slider using session state
        altitude_input = st.slider(
            "Altitude (m)", 
            # min_value=0, 
            max_value=50000, 
            value=st.session_state['altitude'], 
            step=100
        )
        st.session_state['altitude'] = altitude_input  # Update session state with the new value

        # Getting ISA conditions based on session state altitude
        temperature, pressure, density, sound_speed, zone = get_ISA_conditions(st.session_state['altitude'])

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

    spacer('2em')

# ====================
    
    # cruise speed

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


# ====================

    # Drag Coefficient (Cx)

    st.subheader("Lift coefficient at cruise (c_z_krst)")

    
    with st.expander("Calculate Cruise Lift Coefficient"):
        def calculate_c_z_krst():
            c_z_krst.value = (m_sr.value * g.value) / (0.5 * rho.value * v_krst.value**2 * S.value)
            # LaTeX string with variables
            numbers = (
                f"\\frac{{ {m_sr.value:.2f} \\cdot {g.value:.2f} }}"  # Format to two decimal places
                f"{{0.5 \\cdot {rho.value:.6f} \\cdot {v_krst.value:.2f}^2 \\cdot {S.value:.2f} }}"  # Format to two decimal places
            )
            # Formula in LaTeX format
            c_z_krst.formula = f"\\frac{{G}}{{q \\cdot S}} = \\frac{{m_{{sr}} \\cdot g}}{{0.5 \\cdot \\rho \\cdot v_{{krst}}^2 \\cdot S}} \\\\ [2em] = {numbers}"

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
    # st.latex(f"{c_z_krst.latex} = {c_z_krst.value:3f}")

    variables_two_columns(c_z_krst, display_formula=False)
  
    st.markdown('***')

    st.header("Airfoil selection")
            
if __name__ == "__main__":
    main()