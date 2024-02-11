### 9_4_Drag_polar.py ###
import streamlit as st
from variables_manager import initialize_session_state, get_variable_value, get_variable_props, display_variable, update_variables, log_changed_variables
from utils import spacer


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


    # ==================== wing ==================== #
    st.header("Minimal drag coefficient")


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
    st.latex(rf"(C_{{Xmin}})_{{trenje+oblik}} = (C_{{Xmin}})_{{krilo}} + (C_{{Xmin}})_{{trup}} + (C_{{Xmin}})_{{vert.rep}} + (C_{{Xmin}})_{{hor.rep}} = {Cx_min_wings:.4f} + {Cx_min_fuselage:.5f} + {Cx_min_vertical:.5f} + {Cx_min_horizontal:.5f} + {Cx_min_landing_gear:.3f} = {Cx_min_total:.5f}")
    st.latex(rf"(C_{{Xmin}})_{{trenje+oblik}} = {Cx_min_wings:.4f} + {Cx_min_fuselage:.5f} + {Cx_min_vertical:.5f} + {Cx_min_horizontal:.5f} = {Cx_min_total:.5f}")
    
    # Correction factor
    delta_K = st.number_input("Roughness correction factor", value=1.6, format="%.2f", step=0.1)

    # Corrected drag coefficient
    Cx_min_corrected = Cx_min_total * delta_K
    st.latex(rf"(C_{{Xmin}})_{{kor}} = (C_{{Xmin}})_{{trenje+oblik}} \cdot \Delta K = {Cx_min_total:.5f} \cdot {delta_K} = {Cx_min_corrected:.5f}")

    Cx_min_landing_gear = st.number_input("Minimal drag coefficient of the landing gear", value=0.005, format="%.3f")
    
    # Spacer for better layout
    spacer()


    update_variables(page_values, locals())
    log_changed_variables()
    st.markdown("***")

if __name__ == "__main__":
    main()