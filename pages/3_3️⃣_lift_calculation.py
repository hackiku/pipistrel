### 3_lift.py ###

import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, update_variables, log_changed_variables
from utils import spacer
from data import airfoil_data
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re

# ./modules/draw/wing_cutout.png

airfoil_df = pd.DataFrame(airfoil_data, columns=[
    "Name", "M_Re", "alpha_n", "a0", "Cz_max", "letter", "alpha_kr", 
    "Cz_op", "alpha_d", "Cd_min", "Cm_ac", "x_ac", "y_ac"
])

def regex_extract_values(output):
    # Dictionary to hold the extracted values
    extracted_values = {}

    # Regular expressions for each line
    patterns = {
        'Cz': r"KOEFICIJENT UZGONA KRILA\s+Cz\s*=\s*([\d.]+)",
        'Cxi': r"KOEF\. INDUKOVANOG OTPORA KRILA\s+Cxi\s*=\s*([\d.]+)",
        'delta': r"Popravni faktor indukovanog otpora\s+delta\s*=\s*([\d.]+)",
        'a': r"GRADIJENT UZGONA KRILA\s+a\s*=\s*([\d.]+) \[1/o\]",
        'AlfaA': r"aerodinamicki napadni ugao krila\s+AlfaA\s*=\s*([\d.\-]+) \[o\]",
        'AlfaAs': r"aerodinamicki nap\. ugao u korenu\s+AlfaAs\s*=\s*([\d.\-]+) \[o\]",
        'Alfa': r"GEOMETRIJSKI NAPADNI UGAO KRILA\s+Alfa\s*=\s*([\d.\-]+) \[o\]",
        'AlfaN': r"UGAO NULTOG UZGONA KRILA\s+AlfaN\s*=\s*([\d.\-]+) \[o\]",
    }

    # Loop over the patterns and apply each regex
    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            # Convert to float if possible, otherwise keep as string
            try:
                extracted_values[key] = float(match.group(1))
            except ValueError:
                extracted_values[key] = match.group(1)

    return extracted_values

def regex_fortran(output):
    table_data = []
    start_extracting = False
    for line in output.split('\n'):
        if start_extracting:
            # Adjusted regex to include the format '-.000'
            values = re.findall(r"-?\d*\.\d+", line)
            if len(values) == 5:
                y_b2, czmax_ap, czmax_ap_cb_ca, cz_lok, pmax_n_m = map(float, values)
                table_data.append({
                    "y/(b/2)": y_b2,
                    "Czmax ap.": czmax_ap,
                    "Czmax-Cb/Ca": czmax_ap_cb_ca,
                    "Czlok": cz_lok,
                    "Pmax [N/m]": pmax_n_m
                })
        if "y/(b/2)         Czmax ap." in line:
            start_extracting = True  # Begin capturing data from the next line

    # Part 2: Extract final CZmax value
    czmax_final_regex = r"Maksimalni koeficijent uzgona krila CZmax = (\d+\.\d+)"
    czmax_final_match = re.search(czmax_final_regex, output)
    czmax_final_value = float(czmax_final_match.group(1)) if czmax_final_match else None

    return table_data, czmax_final_value

def extract_and_save_section(input_file, output_file, start_pattern):
    # Read the input file
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Find the start of the desired section
    start_index = content.find(start_pattern)
    
    if start_index != -1:
        # Extract from the start pattern to the end
        extracted_content = content[start_index:]
        
        # Save the extracted content to the output file
        with open(output_file, 'w') as output_file:
            output_file.write(extracted_content)
        print(f"Content successfully saved to {output_file.name}")
    else:
        print("Start pattern not found in the file.")

# -------------------- flow separation graph -------------------------

def draw_flow_separation(df, wing_image_path, y_b2_column, czmax_ap_column, czlok_column, czmax_cb_ca_column, czmax_final):
    fig, ax = plt.subplots(figsize=(10, 6)) 
    ax.set_title('Cz distribution along wing span')
    ax.set_xlabel('y/(b/2)')
    ax.set_ylabel('Cz')
    
    img = mpimg.imread(wing_image_path)
    ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto')

    ax.plot(df[y_b2_column], df[czmax_ap_column], label='Czmax ap.', marker='o', linestyle='-')
    ax.plot(df[y_b2_column], df[czlok_column], label='Czlok', marker='x', linestyle='--')
    ax.plot(df[y_b2_column], df[czmax_cb_ca_column], label='Czmax-Cb/Ca', marker='.', linestyle='-')

    separation_point = df[df[czmax_cb_ca_column] == czmax_final]
    if not separation_point.empty:
        sep_point_row = separation_point.iloc[0]
        ax.scatter(sep_point_row[y_b2_column], sep_point_row[czmax_cb_ca_column], color='red', s=100, label='Flow Separation Point')
    else:
        st.error("Flow separation point not found in the data.")
    
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


# ======================================================================#
# ================================ MAIN ================================#
# ======================================================================#

def main():
    
    page_values = [
        'S', 'l0', 'l1', 'b', 'm_sr', 'v_krst', 'T', 'P', 'rho', 'c', 'g', 
        'Re', 'c_z_krst', 'lmbda', 'n', 'phi', 'alpha_n', 'c_z_max_root',
        'alpha_0_root',  'a_0_root', 'c_z_max_tip', 'alpha_0_tip', 'a_0_tip'
    ]
    initialize_session_state(page_values)

    # Display title and headers
    st.title("③ Lift performance ⬆️")
    st.write('The goal of this section is to construct the lift curve, and for that we need to calculate the following parameters:')
    st.markdown(r"""- $C_{z_{max}}$ - Max lift coefficient
- $\alpha_0$ - Zero-lift angle of attack
- $a_0$ - Lift curve slope XXX
- $\alpha_{krst}$ - Angle of attack at cruise
""")
    
    st.markdown("***")    
    st.header("💾 Fortran program")
    st.write("The following values are used in the FORTRAN program below. Values are default unless you calculated them on other pages, and you can change them here as well.")

    spacer('1em')

    # ---------- mission ----------
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### ✏️ Mission parameter inputs')
    with col2:
        with st.expander("Adjust mission parameters"):
            c_z_krst = st.number_input('Cruise Lift Coefficient `c_z_krst`', value=get_variable_value('c_z_krst'), format="%.3f")
            col1, col2 = st.columns(2)
            with col1:
                v_krst = st.number_input('Cruising Speed (m/s) `v_krst`', value=get_variable_value('v_krst'), format="%.3f")
            with col2:
                v_krst_kmh = st.number_input('Cruising Speed (km/h) `v_krst_kmh`', value=get_variable_value('v_krst') * 3.6, format="%.3f")
            rho = st.number_input('Air Density at Cruise Altitude (kg/m^3) `rho`', value=get_variable_value('rho'), format="%.3f")

    
    mission_params_table = f"""
    | # | Parameter                           | Symbol                 | Value                       | Unit    |
    |---|-------------------------------------|------------------------|-----------------------------|---------|
    | 1 | Lift coefficient at cruise          | $C_{{z_{{krst}}}}$     | {c_z_krst:.3f}              | -       |
    | 2 | Cruising speed                      | $v_{{krst}}$           | {v_krst:.3f}                | m/s     |
    | 3 | Cruising speed (km/h)               | $v_{{krst_{{km/h}}}}$  | {v_krst_kmh:.3f}            | Km/h    |
    | 4 | Air density at cruise altitude      | $\\rho$                | {rho:.5f}                   | kg/m³   |
    """
    st.markdown(mission_params_table)
    
    spacer()

    st.markdown('#### 📐 Wing geometry inputs')
    with st.expander("Edit wing dimensions"):
        
        st.write("Calculate wing aspect ratio (λ) `lmbda`")
            
        col1, col2 = st.columns(2)
        with col1:
            b = st.number_input('Wingspan `b` (m)', value=get_variable_value('b'), format='%.3f')
        with col2: 
            S = st.number_input('Wing Area (m^2) `S`', value=get_variable_value('S'), format='%.3f')
        lmbda = b**2 / S
        st.latex(f"\\lambda = \\frac{{b^2}}{{S}} = \\frac{{{b**2:.3f}}}{{{S:.3f}}} = {lmbda:.3f}")
        
        st.write("Calculate wing taper ratio `n`")
        col1, col2 = st.columns(2)
        with col1:
            l0 = st.number_input('Tip Chord Length (m) `l0`', value=get_variable_value('l0'), format='%.3f')
        with col2:
            ls = st.number_input('Root Chord Length (m) `ls`', value=get_variable_value('ls'), format='%.3f')
        n = l0 / ls
        st.latex(f"n = \\frac{{l_0}} {{l_s}} = \\frac{{{l0:.3f}}} {{{ls:.3f}}} = {n:.3f}")


    wing_geometry_table = f"""
    | # | Parameter                           | Symbol                 | Value                       | Unit    |
    |---|-------------------------------------|------------------------|-----------------------------|---------|
    | 1 | Wing Aspect Ratio (λ)               | $\\lambda$             | {lmbda:.3f}                 | -       |
    | 2 | Tip Chord Length                    | $l_0$                  | {l0:.3f}                    | m       |
    | 3 | Root Chord Length                   | $l_s$                  | {ls:.3f}                    | m       |
    | 4 | Wing Taper Ratio (n)                | $n$                    | {n:.3f}                     | -       |
    """
    st.markdown(wing_geometry_table)

    spacer() # ---------- airfoils ----------
    
    st.markdown('#### 🦋 Airfoil data inputs')

    col1, col2 = st.columns(2)
    with col1:
        airfoil_name_root = st.selectbox('🌳 Root airfoil', airfoil_df['Name'].unique(), index=airfoil_df['Name'].tolist().index('NACA 65_2-415, a=0.5'))
        root_airfoil_row = airfoil_df[airfoil_df['Name'] == airfoil_name_root].iloc[0]
    with col2:
        airfoil_name_tip = st.selectbox('🔺 Tip Airfoil', airfoil_df['Name'].unique(), index=airfoil_df['Name'].tolist().index('NACA 65_1-412'))
        tip_airfoil_row = airfoil_df[airfoil_df['Name'] == airfoil_name_tip].iloc[0]

    with st.expander("Show raw airfoil data"):
        col1, col2 = st.columns(2)
        with col1:
            st.text("root_airfoil_row")
            st.code(root_airfoil_row)
        with col2:
            st.text("tip airfoil row")
            st.code(tip_airfoil_row)

    # root airfoil data
    c_z_max_root = root_airfoil_row['Cz_max']
    alpha_0_root = root_airfoil_row['alpha_n']
    a_0_root = root_airfoil_row['a0']

    # tip airfoil data
    c_z_max_tip = tip_airfoil_row['Cz_max']
    alpha_0_tip = tip_airfoil_row['alpha_n']
    a_0_tip = tip_airfoil_row['a0']

    
    airfoil_inputs = f"""
    | # | Parameter                | Symbol                | Root       | Tip                |
    |---|--------------------------|-----------------------|--------------------|-----------------|
    | 1 | Airfoil name             |                       | {airfoil_name_root} | {airfoil_name_tip}   |
    | 2 | Max lift coefficient     | $C_{{z_{{max}}}}$     | {c_z_max_root:.3f}  | {c_z_max_tip:.3f} |
    | 3 | Angle of zero lift       | $\\alpha_0$           | {alpha_0_root:.2f}° | {alpha_0_tip:.2f}° |
    | 4 | Lift gradient            | $a_0$                 | {a_0_root:.3f}      | {a_0_tip:.3f}   |
    """
    st.markdown(airfoil_inputs)
    
    spacer()
    
    st.success("🎉 All values loaded in Fortran code below")
    
    # st.markdown("***")

    fortran_inputs = f"""C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

      IZB=1
      DATA CZ / {c_z_krst:.3f} /  !ZADATI KOEFICIJENT UZGONA KRILA
      DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
C                                          konst.
C              broj    vitkost suzenje   vitop.   brzina   gustina
C            preseka                     [step.]  [km/h]   [kg/m^3]
      DATA      K,       LAM,   EN,       EPS_K,    V,        RO
    &     /    16,       {lmbda:.3f}, {n:.3f},      0.0,  {v_krst_kmh:.2f},    {rho:.3f} /

      DATA CZMAXAP_S / {c_z_max_root:.3f} / ! maks. koef. uzgona ap. u korenu krila
      DATA CZMAXAP_0 / {c_z_max_tip:.3f} / ! maks. koef. uzgona ap. na kraju krila
      DATA AAAP_S / {a_0_root:.3f} / !grad. uzgona ap. u korenu [1/o]
      DATA AAAP_0 / {a_0_tip:.3f} / !grad. uzgona ap. na kraju [1/o]
      !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
      DATA ANAP_S / {alpha_0_root:.1f} / !ugao nultog uzgona ap. u korenu krila [o]
      DATA ANAP_0 / {alpha_0_tip:.1f} / !ugao nultog uzgona ap. na kraju krila [o]
      DATA LS / {ls:.3f} /  ! duzina tetive u korenu krila u metrima

C     ******************** KRAJ UNOSA PODATAKA *************************"""
    st.code(fortran_inputs, language='fortran')

    st.markdown("***")
    
    # ==================== FORTRAN OUTPUT ====================
    extract_and_save_section('./modules/fortran/IZLAZ.TXT', './modules/fortran/short_output.java', 'KARAKTERISTIKE KRILA PRI ZADATOM KOEFICIJENTU UZGONA ILI REZIMU KRSTARENJA')

    with open('./modules/fortran/IZLAZ.TXT', 'r') as file:
        output = file.read()
        
    table_data, czmax_final = regex_fortran(output)

    extracted_values = regex_extract_values(output)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧲 Fortran output")
    with col2:
        st.write(extracted_values)


    if st.button("Show full Fortran text file"):
        st.code(output, language='fortran')

    st.markdown("***")
    
    with open('./modules/fortran/short_output.java', 'r') as file:
        output = file.read()
        st.code(output, language='brainfuck')
    
    #==================== PLOT ====================#
    
    st.header("📈 Flow separation")
    spacer()
    
    st.markdown(f"##### Max lift coefficient `c_z_max`")
    st.latex(f"C_{{z_{{max}}}} = {czmax_final}")
    spacer('1em')

    df = pd.DataFrame(table_data)
    
    # czmax_final = 1.599
    
    df['Highlight'] = df['Czmax ap.'].apply(lambda x: 'Yes' if x == czmax_final else 'No')
    # df['Highlight'] = np.where(df['Czmax ap.'] == czmax_final, 'Yes', 'No')
    
    st.write(df)

    wing_image_path = './modules/draw/wing_cutout.png'
    
    y_b2_column = 'y/(b/2)'
    czmax_ap_column = 'Czmax ap.'
    czlok_column = 'Czlok'
    czmax_cb_ca_column = 'Czmax-Cb/Ca'
    
    draw_flow_separation(df, wing_image_path, 'y/(b/2)', 'Czmax ap.', 'Czlok', 'Czmax-Cb/Ca', czmax_final)

    st.markdown("***")
    
    # ==================== 2. alpha_0 ============================================================
    st.markdown(r"#### 2️⃣ Zero-lift angle of attack – $\\alpha_0$ `alpha_0`")
    
    st.write("The zero lift angle of attack, is a specific angle at which an airfoil or wing generates no lift. It is an aerodynamic characteristic of the airfoil's shape and is determined by its geometry. ")
    st.latex(f"\\alpha_n = {extracted_values['AlfaN']}°")
    
    st.write("Analytical calculation of angle of zero lift:")
    st.latex(f"\\alpha_n = \\alpha_{{ns}} + \\epsilon \cdot f_a")
    st.latex(r"\alpha_n = \alpha_{ns} + \epsilon \cdot f_a")

    st.markdown("""
    - $$ \\alpha_{ns} $$ is the angle of zero lift of the airfoil in the plane of symmetry, $$ \\alpha_{ns} = -1^\\circ $$
    - $$ \\varepsilon $$ is the total twist of the wing, $$ \\varepsilon = \\varepsilon_a + \\varepsilon_k = 0.3^\\circ + 0^\\circ - 0.3^\\circ $$
    - $$ \\varepsilon_a $$ is the aerodynamic twist, $$ \\varepsilon_a = \\alpha_{ns} - \\alpha_{n0} = -1^\\circ - (-1.3^\\circ) \cdot 0.3^\\circ $$
    - $$ \\varepsilon_k $$ is the constructive twist, $$ \\varepsilon_k = 0^\\circ $$ (as there is no constructive twist)
    """)

    st.markdown("***")
    # ==================== 3. a_0 ============================================================
    
    st.markdown("#### 3️⃣ Lift Gradient – $a$ `a`")
    st.latex(r"a = \frac{a_0 \cdot \lambda}{2 + \sqrt{4 + \lambda^2 \cdot \beta^2 \cdot \left(1 + \frac{\tan^2(\phi)}{\beta^2}\right)}} = \frac{0.110 \cdot 3.888}{2 + \sqrt{4 + (3.888)^2 \cdot (0.71)^2 \cdot \left(1 + \frac{\tan^2(27^\circ)}{(0.71)^2}\right)}} = 0.07197 \approx 0.072")
    
    st.markdown("***")
    
    
    
    # ==================== 4. alpha_krst ============================================================
    st.markdown("#### 4️⃣ Critical angle of attack – $\\alpha_{{kr}}$ `alpha_kr`")

    st.code("NACA 65-206 # tip")
    st.code("NACA 64-209 # root")
    # Definitions in Markdown
    st.markdown("""
        The critical angle of attack is used to determine the angle at which the wing will stall. It is calculated using the following formula:

    - $ \\alpha_{kr} $ critical airfoil angle of attack at flow separation
    - $ \\alpha_{nm} $ is the zero-lift angle of attack at the wing's mid-span.
    - $ \\alpha_{ns} $ is the zero-lift angle of attack at the root (in the plane of symmetry).
    - $ \\alpha_{n0} $ is the zero-lift angle of attack at the wingtip.
    - $ \\alpha_{im} $ is the induced angle of attack at the wing's mid-span.
    - $ C_{z_{max}} $ is the maximum lift coefficient.
    - $ \\lambda $ is the wing aspect ratio.
    - $ \\epsilon_{m} $ is the washout angle at the wing's mid-span.
    - $ \\alpha_{kr} $ is the critical angle of attack of the wing.

    The formulas are as follows:
    """)

    # alpha krm
    alpha_kr_tip = tip_airfoil_row['alpha_kr']
    alpha_kr_root = root_airfoil_row['alpha_kr']
    y_b_2 = 0.556 # TODO extract
    
    alpha_krm = alpha_kr_root*(1 - (1 - alpha_kr_root/alpha_kr_tip)*y_b_2)
        
    # Alpha nm calculation

    alpha_n_root = root_airfoil_row['alpha_n']
    alpha_n_tip = tip_airfoil_row['alpha_n']
    alpha_nm = alpha_n_root*(1 - (1 - alpha_n_tip/alpha_n_root)*y_b_2) 

    # Alpha im calculation
    cz_max = 0.922  # Maximum lift coefficient
    lmbda = 3.358  # Wing aspect ratio
    alpha_im = cz_max / (3.14159 * lmbda) * 57.3 # Induced angle of attack

    # Epsilon m calculation
    epsilon_k = -5  # Geometric washout angle
    epsilon_m = -3.17  # The calculated value for epsilon_m

    # Alpha kr calculation
    alpha_kr = 22.122  # The calculated value for alpha_kr
    
    # Insert the calculated values into the LaTeX string
    st.latex(f"\\alpha_{{kr m}} = \\alpha_{{krs}} \\left( 1 - \\left(1 - \\frac{{\\alpha_{{kro}}}}{{\\alpha_{{krs}}}}\\right)\\frac{{y}}{{b}}\\right) = {alpha_kr_root} \\left( 1 - \\left(1 - \\frac{{{alpha_kr_tip}}}{{{alpha_kr_root}}}\\right)\\frac{{{y_b_2}}}{{2}}\\right) = {alpha_krm:.4f}°")
    st.latex(f"\\alpha_{{nm}} = \\alpha_{{ns}} \\left( 1 - \\left(1 - \\frac{{\\alpha_{{n0}}}}{{\\alpha_{{ns}}}}\\right)\\frac{{y}}{{b}}\\right) = {alpha_n_root:.4f} \\left( 1 - \\left(1 - \\frac{{{alpha_n_tip}}}{{{alpha_n_root}}}\\right){y_b_2}\\right) = {alpha_nm}°")
    st.latex(f"\\alpha_{{im}} = \\frac{{C_{{z_{{max}}}}}}{{\\pi \\cdot \\lambda}} \\cdot 57.3 = \\frac{{{cz_max}}}{{\\pi \\cdot {lmbda}}} \\cdot 57.3 = {alpha_im:.4f}°")
    st.latex(f"\\epsilon_{{m}} = \\epsilon_{{k}} \\frac{{y}}{{b}} = {epsilon_k} \\cdot {y_b_2} = {epsilon_m}°")
    st.latex(f"\\alpha_{{kr}} = {alpha_nm}° - ({alpha_nm}°) + ({alpha_n_root}°) - ({epsilon_m}°) + {alpha_im}° = {alpha_kr}°")

    st.markdown("***")
    # Update variables at the end of the session
    update_variables(page_values, locals())
    log_changed_variables()

if __name__ == "__main__":
    main()