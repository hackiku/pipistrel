
############ sessionstate.py
############ app/pages/sessionstate.py
import streamlit as st
import inspect

def main():
    st.title("Ultimate variable tracker")

    ############ for loop to iterate main.py and all pages in pages folder
    ############ add st.header for each page name
    inspect ############ inspect code that uses Variable class and list as st.code

if __name__ == "__main__":
    main()
    

# ============ relevant parts from other pages, chatgpt ============

############ main.py - see how Variables are defined. Sometimes other pages rewrite them, too

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import inspect
from data import Variable, save_variables_to_session, load_variables_from_session, aircraft_specs, create_specs_table 
from isa_lite import get_ISA_conditions
from utils import spacer
from pages import draw_hifi

############ this is how variables are defined
# wing geometry
S = Variable("Wing Area", 30.00, "S", "S", "m²")
l0 = Variable("Root Chord Length", 1.00, "l0", "l_{0}", "m")
l1 = Variable("Tip Chord Length", 2.00, "l1", "l_{1}", "m")
b = Variable("Wingspan", 40.00, "b", "b", "m")

# mission parameters
m_sr = Variable("Average mass", 100.00, "m_sr", "m_{sr}", "kg")
v_krst = Variable("Cruising speed", 50.00, "v_krst", r"v_{krst}", "m/s")
rho = Variable("Air density at altitude", 0.05, "rho", r"\rho", "kg/m^3")
g = Variable("Gravity acceleration", 9.80665, "g", "g", "m/s²")
c_z_krst = Variable("Cruise lift coefficient", 0.200, "c_z_krst", r"C_{z_{krst}}", "")


# use data points in calculations
def get_specific_data(df, category):
    category_data = df[df['Specification'] == f"**{category}**"]
    if not category_data.empty:
        start_index = category_data.index[0] + 1
        end_index = df[df['Specification'].str.startswith('**', na=False)].index
        end_index = end_index[end_index > start_index].min()

        return df[start_index:end_index]
    return pd.DataFrame()



############ data.py
import streamlit as st
import pandas as pd

############ Variable class constructor
class Variable:
    def __init__(self, name, value, python, latex='', unit='', value2=None, unit2='', formula=''):
        self.name = name
        self.value = value
        self.python = python
        self.latex = latex or name  # Fallback to name if no latex is provided
        self.unit = unit
        self.value2 = value2
        self.unit2 = unit2
        self.formula = formula
    
    def save_to_session(self):
        st.session_state[self.latex] = self

############ functions to load to session state. Probably best to drop them into this new python page instead
def save_variables_to_session(variables_dict):
    for var_name, var_value in variables_dict.items():
        if isinstance(var_value, Variable):
            st.session_state[var_value.python] = var_value  # Use python attribute for session state key
            st.code(f"{var_value.python} = {var_value.value} {var_value.unit} # {var_value.name}")
    
def load_variables_from_session(variable_names):
    loaded_variables = {}
    code_display = "" 
    for name in variable_names:
        variable = st.session_state.get(name)
        if variable:
            loaded_variables[name] = variable
            code_display += f"{name}: {variable.value} {variable.unit} # {variable.name} \n"
    return loaded_variables, code_display
# ....



############ 3_wing_pg.py - see how Variables are loaded from session state

import streamlit as st
from main import main as initialize_main
from data import Variable, save_variables_to_session, load_variables_from_session
from utils import spacer, variables_two_columns, display_generic_table
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import re
from main import (S as S_home, l0 as l0_home, l1 as l1_home, b as b_home, 
v_krst as v_krst_home, rho as rho_home, c_z_krst as c_z_krst_home, main as run_hompeage)




# Hardcoded Airfoil Data
root_airfoil_data = ["NACA 65_2-415", 9.0, -2.8, 0.113, 1.62, "D", 16.5, 0.30, 11.5, 0.0040, -0.062, 0.266, -0.062]
tip_airfoil_data = ["NACA 63_4-412", 9.0, -3.0, 0.100, 1.78, "D", 15.0, 0.32, 9.6, 0.0045, -0.075, 0.270, -0.073]

# Extracting specific values from airfoil data
c_z_max_root = Variable("Max Lift Coefficient at Root", root_airfoil_data[4], "c_z_max_root", r"C_{z_{max}}", "")
alpha_0_root = Variable("Angle of Zero Lift at Root", root_airfoil_data[2], "alpha_0_root", r"\alpha_{0}", "degrees")
a_0_root = Variable("Lift Gradient at Root", root_airfoil_data[3], "a_0_root", r"a_{0}", "")

c_z_max_tip = Variable("Max Lift Coefficient at Tip", tip_airfoil_data[4], "c_z_max_tip", r"C_{z_{max}}", "")
alpha_0_tip = Variable("Angle of Zero Lift at Tip", tip_airfoil_data[2], "alpha_0_tip", r"\alpha_{0}", "degrees")
a_0_tip = Variable("Lift Gradient at Tip", tip_airfoil_data[3], "a_0_tip", r"a_{0}", "")

# geometry calcs
lambda_wing = Variable("Wing Aspect Ratio", 3.888, r"\lambda")
n = Variable("Wing Taper Ratio", 0.520, "n", "n")
phi = Variable("Sweep Angle", 27, "phi", r"\phi", "degrees")
alpha_n = Variable("Angle of Attack", -1.3, "alpha_n", r"\alpha_n", "degrees")

# c_z_max = Variable("Max Lift Coefficient", 1.148, r"C_{z_{max}}", "")

def main():
    ############ see how we load variables from state. it's clunky and verbose. i'd rather abstarct this to the SESSIONSTATE file
    ############ but ill need a way to explicitly load variables needed (if they dont, default values load automagically)
    # load variables from state
    variable_names_to_load = ['S', 'l0', 'l1', 'b', 'v_krst', 'rho', 'g', 'm_sr', 'c_z_krst']
    variables, code = load_variables_from_session(variable_names_to_load)
    st.code(code)
    
    S = variables.get('S', S_home)
    l0 = variables.get('l0', l0_home)
    l1 = variables.get('l1', l1_home)
    b = variables.get('b', b_home)
    v_krst = variables.get('v_krst', v_krst_home)
    rho = variables.get('rho', rho_home)
    c_z_krst = variables.get('c_z_krst', c_z_krst_home)
        
    st.code(f"S = {S.value}, l0 = {l0.value}, l1 = {l1.value}, b = {b.value}, v_krst = {v_krst.value}, rho = {rho.value}, c_z_krst = {c_z_krst.value}")
    st.title("3. Wing Design")