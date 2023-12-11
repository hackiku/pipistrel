# utils.py
import streamlit as st

def spacer(height='5em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

def variables_two_columns(var, display_formula=False):
    col1, col2 = st.columns([2,3])
    with col1:
        new_value = st.number_input(var.name, value=var.value, step=0.001, format="%.3f")
        var.value = new_value  # Update the variable's value
    with col2:
        if display_formula and var.formula:
            spacer('2em')
            st.markdown(f"$${var.formula}$$")
        else:
            # Otherwise, display the LaTeX representation with the value and unit
            st.markdown(f"$${var.latex} = {var.value:.3f} \ {var.unit}$$")
          
