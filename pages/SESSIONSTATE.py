# SESSIONSTATE.py
# app/pages/SESSIONSTATE.py
import streamlit as st
import inspect

def main():
    st.warning("This is a work in progress. Please do not share this app.")

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
