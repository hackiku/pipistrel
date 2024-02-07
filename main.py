### app.py ###
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from data import aircraft_specs, create_specs_table 
from utils import spacer
from modules.isa_lite import get_ISA_conditions
from variables_manager import initialize_session_state, get_variable_value, \
    update_variables, log_changed_variables, rewrite_default_values
from pages.draw_wing_areas import draw_wing_area

# TODO abstract wingspan
def calculate_wingspan(shapes):
    conversion_hardcoded = 0.00584518884292006
    
    min_x = float('inf')  # Initialize with infinity
    max_x = float('-inf') # Initialize with negative infinity

    # Iterate through each shape and update min and max x-coordinates
    for shape in shapes:
        for line in shape.lines:
            start_x, end_x = line['start'][0], line['end'][0]
            min_x = min(min_x, start_x, end_x)
            max_x = max(max_x, start_x, end_x)

    # Calculate wingspan as the difference between max and min x-coordinates
    wingspan = (max_x - min_x) * conversion_hardcoded
    return wingspan


# aircraft specs from POH
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

# ==========================================================
# ========================== main ==========================
# ==========================================================
def main():
    
    page_values = [
        'S', 'l0', 'ls', 'b', 'm_sr', 'H', 'T', 'P', 'rho', 'c', 
        'g', 'nu', 'v_max_percent', 'v_krst', 'Re', 'c_z_krst',
        'm_empty', 'm_max'
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
    st.title("① Mission planner")
    st.write("This tool will help you plan your aircraft's mission by calculating the lift coefficient at cruise conditions.")

    spacer()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("🛩️ Aircraft specs")
    with col2:
        unit_system = st.radio("", ('SI Units', 'Aviation Units'))

    # specs tablez
    all_specs_df = create_specs_table(aircraft_specs)
    preset = st.selectbox("Select Preset", ["Airfoil", "All"], index=0)
    filtered_df = filter_data_for_preset(all_specs_df, preset)
    st.table(filtered_df)

    st.markdown('***')

# ==================== IMAGE ====================#

    st.header("📐 Wing geometry")
    spacer('2em')

    # svg_file_path = './modules/draw/wing_area/wing_single.svg'
    svg_file_path = './modules/draw/wing_area/wing_single.svg'
    shapes = draw_wing_area(svg_file_path)

    S0 = shapes[0].area
    S1 = shapes[1].area
    Spr = S0 + S1
    S = Spr * 2
    l0 = shapes[0].lines[0]['length_meters']
    ls = shapes[0].lines[2]['length_meters']
    wing_length = calculate_wingspan(shapes)
    b = wing_length * 2

    col1, col2, col3 = st.columns(3)
    with col1:
        st.text("Tip length")
        st.latex(f"l_0 = {l0:.3f}  \\, \\text{{m}}")
    with col2:
        st.text("Root length")
        st.latex(f"l_s = {ls:.3f}  \\, \\text{{m}}")
    with col3:
        st.text("Wingspan")
        st.latex(f"b = {wing_length:.3f} \\cdot 2 = {b:.3f}  \\, \\text{{m}}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.latex(f"S_0 = {S0:.3f}  \\, \\text{{m}}^2")
    with col2:
        st.latex(f"S_1 = {S1:.3f}  \\, \\text{{m}}^2")
    with col3:
        st.latex(f"S_{{pr}} = S_{{0}} + S_{{1}} = {Spr:.3f} \\, \\text{{m}}^2")
    
    st.latex(f"S = S_{{pr}} \\cdot 2 = {Spr:.3f} \\cdot 2 = {S:.3f} \\, \\text{{m}}^2")

    # sweepback angle
    # st.latex(r"\varphi = \frac{\varphi_{UN} \cdot S_{UN} + \varphi_{SP} \cdot S_{SP}}{S}")

    st.markdown('***')

#==================== MASS ====================#

    st.subheader('🧲 Average mass')
    spacer('1em')
    
    m_empty_poh = aircraft_specs["Weights"]["Design Empty Weight"]["value"]
    m_max_poh = aircraft_specs["Weights"]["Max Take Off Weight"]["value"]

    if st.button('⚠️ Reload POH values'):
        reload_poh = True
    else:
        reload_poh = False
        
    m_empty_default = m_empty_poh if reload_poh else get_variable_value('m_empty') or m_empty_poh
    m_max_default = m_max_poh if reload_poh else get_variable_value('m_max') or m_max_poh

    # max takeoff weight & design empty weight
    col1, col2 = st.columns(2)
    with col1:
        m_empty = st.number_input("Design Empty Weight (kg) `m_empty`", value=m_empty_default, min_value=1, step=20)
    with col2:
        m_max = st.number_input("Max Take Off Weight (kg) `m_max`", value=m_max_default, min_value=m_empty, step=20)

    # Calculate average mass
    m_sr = (m_max + m_empty) / 2
    
    st.latex(f"m_{{\\text{{sr}}}} = \\frac{{m_{{\\text{{max}}}} + m_{{\\text{{min}}}}}}{2} = \\frac{{{m_max:.2f} + {m_empty:.2f}}}{2} = {m_sr:.3f} \\, \\text{{kg}}")

    st.markdown('***')

# ==================== ISA ====================#
    # ./modules/isa_lite.py
    
    st.subheader("🌤️ ISA air conditions")
    spacer('1.5em')

    col1, col2 = st.columns(2)
    
    # altitude slider
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

    with col2: # latex values
        st.latex(f"H = {H} \, \ {{m}} \, \ ({H * 3.28084:.0f} \, \ {{ft}})")
        st.latex(f"T = {T:.2f} \, \ {{K}} \, ({T - 273.15:.2f} \ {{°C}})")
        st.latex(f"P = {P:.2f} \, \ {{Pa}}")
        st.latex(f"\\rho = {rho:.5f} \, \ {{kg/m}}^3")
        st.latex(f"c = {c:.2f} \, \ {{m/s}}")

    spacer()
    st.text('Kinematic viscosity calculated with the Sutherland formula: ')
    nu = (1.458e-6 * T**1.5) / (T + 110.4) / rho
    st.latex(r'\nu = \frac{\mu}{\rho} = \frac{1.458 \times 10^{-6} \cdot T^{1.5}}{T + 110.4} \cdot \frac{1}{\rho}')
    st.latex(f'\\nu = {nu:.2e} \\, \\text{{m}}^2/\\text{{s}}')
        
    st.markdown('***')

# ==================== SPEED ====================#
    
    col1, col2 = st.columns([3,1])
    with col1:
        st.subheader("⚡️ Cruise speed")
    with col2:
        st.write()
        # unit = st.radio("", ['Km/h', 'm/s'])
    spacer('1.5em')

    v_max_poh = aircraft_specs["Performance"]["Max Structural Cruising Speed"]["value"]
    
    st.write(f"Pick the cruise speed as % of max structural cruising speed ({v_max_poh} Km/h), usually 70-80%")

    col1, col2, col3 = st.columns([4, 1, 2])
    with col1:
        v_max_percent = st.slider("Percentage of `v_max` (%)", value=get_variable_value('v_max_percent'), min_value=0, max_value=100, step=1)
    with col2:
        unit = st.radio("", ['Km/h', 'm/s'])
    with col3:
        if unit == 'Km/h':
            v_max = st.number_input("Max structural speed (Km/h)", value=v_max_poh, min_value=0.00, step=10.00)
            v_krst = v_max_percent / 100.0 * (v_max / 3.6)  # Convert to m/s
        else:
            v_max = st.number_input("Max structural cruise speed", value=v_max_poh / 3.6, min_value=0.00, step=1.00)
            v_krst = v_max_percent / 100.0 * v_max  # Already in m/s

    st.latex(f"v_{{\\text{{krst}}}} = \\frac{{v_{{max}} \\times {v_max_percent}\\%}}{{100}} = \\frac{{{v_max:.3f} \\times {v_max_percent}}}{{100}}")
    st.latex(f"v_{{\\text{{krst}}}} = {v_krst*3.6:.3f} \\, \\text{{Km/h}} = {v_krst:.3f} \\, \\text{{m/s}}")

    st.markdown('***')


#==================== LIFT COEFF ====================#

    st.subheader("🎈 Lift coefficient at cruise")
    spacer('1.5em')

    # toggle planet
    planet = st.radio("Select Planet", ['🌎 Earth', '🟠 Mars'], horizontal= True, index=0)

    # manual changes
    with st.expander("Manually recalculate `cz_krst`"):

        col1, col2, col3 = st.columns(3)
        with col1:
            S_manual = st.number_input(f'Wing area (m²) `S`', value=S, step=0.1, format="%.5f")
            S = S_manual
        with col2:
            m_sr_manual = st.number_input('Average mass (kg) `m_sr`', value=m_sr, step=20.0, format="%.3f")
            m_sr = m_sr_manual
        with col3:
            v_krst_manual = st.number_input('Cruise speed (m/s) `v_krst`', value=v_krst, step=1.0, format="%.5f")
            v_krst = v_krst_manual

        spacer()

        # planet selector
        col1, col2, col3 = st.columns(3)
        with col1:
            if planet == '🌎 Earth':
                altitude = st.number_input("Altitude (m)", value=H, min_value=0, step=100)
                temperature, pressure, density, sound_speed, zone = get_ISA_conditions(altitude)
                g_planet = 9.80665
            elif planet == '🟠 Mars':
                g_planet = 3.72076
                density = 0.020
                spacer('1em')
                st.warning(f"🪐 Mars")
        with col2:
            g = st.number_input('Gravity', value=g_planet, step=0.01, format="%.5f")
        with col3:
            rho = st.number_input(f'Density $${{kg/m}}^3$$ `rho`', value=density, step=0.001, format="%.5f")
            # rho = st.number_input(f'Density', value=rho.value, step=0.001, format="%.5f")

    c_z_krst = (m_sr * g) / (0.5 * rho * v_krst**2 * S)
    st.latex(r"C_{Z_{krst}} = \frac{G}{q \cdot S} = \frac{m_{sr} \cdot g}{0.5 \cdot \rho \cdot v_{krst}^2 \cdot S}")
    st.latex(f"C_{{Z_{{krst}}}} = \\frac{{ {m_sr:.3f} \\cdot {g:.3f} }}{{ 0.5 \\cdot {rho:.4f} \\cdot {v_krst:.3f}^2 \\cdot {S:.3f} }}")
    st.latex(f"C_{{Z_{{krst}}}} = {c_z_krst:.3f}")
    
    st.markdown('***')
    #==================== SESSION STATE ====================#

    update_variables(page_values, locals())
    log_changed_variables()
    
    # danger zone!!
    if st.button('⚠️ Rewrite default values'):
        rewrite_default_values()
    
if __name__ == "__main__":
    main()