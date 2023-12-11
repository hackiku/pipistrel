# utils.py
import streamlit as st

def spacer(height='5em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

def variables_two_columns(var):
    col1, col2 = st.columns([2,3])
    with col1:
        new_value = st.number_input(var.name, value=var.value, step=0.1, format="%.3f")
        var.value = new_value  # Update the variable's value
    with col2:
        # Display the LaTeX representation along with the value and unit
        st.markdown("` `")
        formatted_value = f"{var.value:.3f}"  # This formats the value to 3 decimal places
        st.markdown(f"$${var.latex} = {formatted_value} \ {var.unit}$$")
