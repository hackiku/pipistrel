### 9_4_Drag_polar.py ###
import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, get_variable_props, display_variable, update_variables, log_changed_variables
from utils import spacer
import math


def calculate_induced_drag(Cx_min, phi, b, s, n):

    # Calculate k factor based on the wing sweep angle
    if phi == 0:
        k = 0.38 * Cx_min
    elif phi == 20:
        k = 0.4 * Cx_min
    elif phi == 35:
        k = 0.45 * Cx_min
    else:
        k = 0.4 * Cx_min  # Default case if angle not in table
    
    # Calculate lambda (aspect ratio)
    aspect_ratio = (b**2) / s
    
    # Calculate correction factor 'w' for total induced drag
    w = 1 / (1 + (0.3 / aspect_ratio))
    
    # Calculate delta (induced drag coefficient) using given formula
    phi_radians = math.radians(phi)  # Convert sweep angle to radians for cosine calculation
    delta = 0.02 / math.cos(phi_radians) * ((3.1 - (14 * n) + (20 * n**2) - (8 * n**3)))
    
    return k, aspect_ratio, w, delta

def main():
    page_values = [
        'S', 'S_20', 'S_21', 'S_wet_kr', 'lT', 'l0', 'nT', 
        'l_sat_kr', 'Re', 'v_krst', 'Cf_kr', 'dl_eff_kr', 'K_kr', 'C_X_min_krilo'
    ]
    initialize_session_state()



    
    #==================== drag ====================#
    st.title("4. Drag polar")
    
    st.write("""Proračun otpora aviona (za nestišljivo strujanje. Za ovaj proračun proračun potrebno je:
- Definisati sve dimenzije elemenata konstrukcije aviona potrebne za proračun otpora;
- Odrediti jednačinu polare aviona;
- Izračunati maksimalnu finesu aviona i CZ pri kome se ona ostvaruje;
- Odrediti finesu aviona i potrebnu vučnu silu elise na režimu krstarenja;
- Dijagramski pokazati polaru aviona i finesu aviona u funkciji od CZ.""")

    st.markdown("***")    


    # ==================== cxmin ==================== #
    st.header("1. Minimal drag coefficient")


    # Sum of individual minimal drag coefficients
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        Cx_min_wings = st.number_input("Minimal drag coefficient of the wheel", value=0.005, format="%.3f")
    with col2:
        Cx_min_fuselage = st.number_input("Minimal drag coefficient of the fuselage", value=0.005, format="%.3f")
    with col3:
        Cx_min_vertical = st.number_input("Minimal drag coefficient of the empennage", value=0.005, format="%.3f")
    with col4:
        Cx_min_horizontal = st.number_input("Minimal drag coefficient of the vent", value=0.005, format="%.3f")
    
    Cx_min_total = Cx_min_wings + Cx_min_fuselage + Cx_min_vertical + Cx_min_horizontal
    st.latex(rf"(C_{{Xmin}})_{{trenje+oblik}} = (C_{{Xmin}})_{{krilo}} + (C_{{Xmin}})_{{trup}} + (C_{{Xmin}})_{{vert.rep}} + (C_{{Xmin}})_{{hor.rep}}")
    st.latex(rf"(C_{{Xmin}})_{{trenje+oblik}} = {Cx_min_wings:.4f} + {Cx_min_fuselage:.5f} + {Cx_min_vertical:.5f} + {Cx_min_horizontal:.5f} = {Cx_min_total:.5f}")
    
    spacer()
    
    # corrected cx_min
    delta_K = st.number_input("Roughness correction factor", value=1.6, format="%.2f", step=0.1)
    Cx_min_corrected = Cx_min_total * delta_K
    st.latex(rf"(C_{{Xmin}})_{{kor}} = (C_{{Xmin}})_{{trenje+oblik}} \cdot \Delta K = {Cx_min_total:.5f} \cdot {delta_K} = {Cx_min_corrected:.5f}")

    # landing gear
    spacer()
    Cx_min_landing_gear = st.number_input("Minimal drag coefficient of the landing gear", value=0.005, format="%.3f")
    Cx_min = Cx_min_corrected + Cx_min_landing_gear
    st.latex(rf"C_{{Xmin}} = (C_{{Xmin}})_{{kor}} + (C_{{Xmin}})_{{trenje+oblik}} = {Cx_min_corrected:.5f} + {Cx_min_landing_gear:.3f} = {Cx_min:.5f}")
    
    spacer()

    # ================================================= #
    # ==================== induced ==================== #
    # ================================================= #

    st.header("2. Induced Drag Calculation")

    # Input values
    phi = st.number_input("Wing sweep angle (φ) in degrees", value=24.00, format="%.1f")
    b = st.number_input("Wingspan (b) in meters", value=9.55, format="%.2f")
    s = st.number_input("Wing area (s) in square meters", value=22.485, format="%.3f")
    n = st.number_input("Load factor (n)", value=0.3, format="%.1f")
    
    # Calculate induced drag
    k, aspect_ratio, w, delta = calculate_induced_drag(Cx_min, phi, b, s, n)
    
    # Display results
    st.write(f"Aspect Ratio (λ): {aspect_ratio:.2f}")
    st.write(f"Correction Factor (w): {w:.4f}")
    st.write(f"Induced Drag Coefficient (δ): {delta:.5f}")

    # LaTeX representation of the calculation
    st.latex(rf"k = 0.40 \cdot C_{{X_{{min}}}} = 0.40 \cdot {Cx_min:.5f} = {k:.5f}")
    st.latex(rf"\lambda = \frac{{b^2}}{{s}} = \frac{{{b:.2f}^2}}{{{s:.3f}}} = {aspect_ratio:.2f}")
    st.latex(rf"w = \frac{{1}}{{1+\frac{{0.3}}{{\lambda}}}} = \frac{{1}}{{1+\frac{{0.3}}{{{aspect_ratio:.2f}}}}} = {w:.4f}")
    st.latex(rf"\delta = \frac{{0.02}}{{\cos(\phi)}} \cdot (3.1 - 14n + 20n^2 - 8n^3) = \frac{{0.02}}{{\cos({phi:.1f}°)}} \cdot (3.1 - 14 \cdot {n} + 20 \cdot {n}^2 - 8 \cdot {n}^3) = {delta:.5f}")



    update_variables(page_values, locals())
    log_changed_variables()
    st.markdown("***")

if __name__ == "__main__":
    main()