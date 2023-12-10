import streamlit as st
import inspect
from calcs import * 
from data import aircraft_specs

c_z_max = 0.240
c_z_max = {"value" = 0.240; "latex" = "latex"}


def main():

  st.title("3. Wing design")
  st.write("Creating lift curve using 4 parameters.")

  st.header("3.1. Wing lift features")

  with st.expander("Explanation"):
    st.markdown(f"""We need 4 parameters blabla
    - Max lift coefficient {c_z_max} 
    """, unsafe_allow_html=True)
  

if __name__ == "__main__":
    main()