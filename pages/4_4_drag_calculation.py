# 4_drag_calculation.py

import streamlit as st
from data import Variable, save_variables_to_session, load_variables_from_session
from main import c_z_krst as c_z_krst_home, v_krst as v_krst_home, S as S_home, b as b_home

bk_fortran_inputs_bk = """C     *************** UNOS ULAZNIH PODATAKA I OPCIJA *******************

C     IZBOR PRORACUNSKE OPCIJE: ZA VREDNOOST IZB=1 RACUNA SA UNAPRED
C     ZADATIM KOEFICIJENTOM UZGONA KRILA CZ; U SUPROTNOM, ZA SVAKI
C     DRUGI INTEGER (npr. IZB=0) CZ RACUNA NA OSNOVU SPECIFICNOG
C     OPTERECENJA KRILA, BRZINE I GUSTINE NA REZIMU KRSTARENJA

      IZB=1
      DATA CZ / {c_z_krst.value:.3f} /  !ZADATI KOEFICIJENT UZGONA KRILA
      DATA SPECOP /800. / !ZADATO SPECIFICNO OPTERECENJE KRILA [N/m^2]

C             PARAMETRI GEOMETRIJE KRILA I REZIMA KRSTARENJA:
C                                          konst.
C              broj    vitkost suzenje   vitop.   brzina   gustina
C            preseka                     [step.]  [km/h]   [kg/m^3]
      DATA      K,       LAM,   EN,       EPS_K,    V,        RO
     &     /    16,      {lambda_wing.value:.2f},   {n.value:.3f},      0.0,    {v_krst.value:.2f},    {rho.value:.6f} /

      DATA CZMAXAP_S / {c_z_max_root.value:.3f} / ! maks. koef. uzgona ap. u korenu krila
      DATA CZMAXAP_0 / {c_z_max_tip.value:.3f} / ! maks. koef. uzgona ap. na kraju krila
      DATA AAAP_S / {a_0_root.value:.3f} / !grad. uzgona ap. u korenu [1/o]
      DATA AAAP_0 / {a_0_tip.value:.3f} / !grad. uzgona ap. na kraju [1/o]
      !teorijska  vrednost gradijenta uzgona 2PI = 0.1096622 [1/o]
      DATA ANAP_S / {alpha_0_root.value:.1f} / !ugao nultog uzgona ap. u korenu krila [o]
      DATA ANAP_0 / {a_0_tip.value:.1f} / !ugao nultog uzgona ap. na kraju krila [o]
      DATA LS / {l1.value:.3f} /  ! duzina tetive u korenu krila u metrima

C     ******************** KRAJ UNOSA PODATAKA *************************"""


def main():
    # Attempt to load variables from session state
    loaded_variables = load_variables_from_session(['c_z_krst', 'b', 'S'])

    # Use values from session state if available; otherwise, use default values
    c_z_krst = loaded_variables.get('c_z_krst', c_z_krst_home)
    b = loaded_variables.get('b', b_home)
    S = loaded_variables.get('S', S_home)
    
    # Show the values after attempting to load from session state
    st.code(f"czkrst state = {c_z_krst.value}")
    st.code(f"b state = {b.value}")
    st.code(f"S state = {S.value}")

    # Calculate the wing aspect ratio
    lambda_wing = Variable("Wing Aspect Ratio", b.value**2 / S.value, r"\lambda")
    
    # Display the variables and the calculated aspect ratio
    st.write(f"Wingspan (b): {b.value} m")
    st.write(f"Wing Area (S): {S.value} m²")
    st.write(f"Wing Aspect Ratio (λ): {lambda_wing.value}")

    #==================== SESSION STATE ====================#
    st.markdown('***')
    st.text("Variables saved to session state:")
    variables_dict = {
        'c_z_krst': c_z_krst,
        'b': b,
        'S': S,
        'lambda_wing': lambda_wing,
    }
    
    # Update session state with the new values
    save_variables_to_session(variables_dict)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
