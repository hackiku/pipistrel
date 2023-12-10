import streamlit as st

# Define a class to hold the variable and its LaTeX representation
class Variable:
    def __init__(self, value, latex, unit='', value2=None, unit2=''):
        self.value = value
        self.latex = latex
        self.unit = unit
        self.value2 = value2
        self.unit2 = unit2

    def __str__(self):
        # This will allow you to simply print the variable to get a string with LaTeX and units
        value_str = f"{self.value} {self.unit}" if self.unit else f"{self.value}"
        if self.value2 is not None:
            value2_str = f"{self.value2} {self.unit2}" if self.unit2 else f"{self.value2}"
            return f"{self.latex}: {value_str}, {value2_str}"
        else:
            return f"{self.latex}: {value_str}"

# Initialize the variables with optional parameters
c_z_max = Variable(0.247, "C_{z_{max}}")
v_krst = Variable(224.37, "v_{krst}", "m/s", 807.73, "km/h")
alpha_n = Variable(-1.3, r"\alpha_n", "degrees")
lambda_wing = Variable(3.888, r"\lambda")
n = Variable(0.520, "n")
rho = Variable(0.736116, r"\rho", "kg/m^3")

def main():
    st.title("3. Wing Design")
    st.write("Creating lift curve using 4 parameters.")
    
    st.header("3.1 Wing Lift Features")

    with st.expander("Explanation"):
        st.markdown(f"""placeholder ignore now""", unsafe_allow_html=True)

    # Use the __str__ method of the Variable class to simplify displaying variables
    st.markdown(f"""
    We need 4 parameters:
    - Max lift coefficient (c_z_max): ${c_z_max}$ = 
    - Gradient of lift curve (alpha_n): ${alpha_n}$
    - Wing aspect ratio (lambda_wing): ${lambda_wing}$
    - Wing taper ratio (n): ${n}$
    - Cruising speed (v_krst): ${v_krst}$
    - Air density at cruise altitude (rho): ${rho}$
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
