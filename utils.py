# utils.py
import streamlit as st

def spacer(height='2em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)
    
def variables_two_columns(var, display_formula=False):
    col1, col2 = st.columns([2,3])
    with col1:
        new_value = st.number_input(var.name, value=var.value, step=0.001, format="%.3f")
        var.value = new_value  # Update the variable's value
        # var.formula.strip"{numbers}"
    with col2:
        if display_formula and var.formula:
            spacer('2em') # verticlal align formula with input
            st.markdown(f"$${var.formula} = {var.value:.3f} \ {var.unit}$$")
        else:
            spacer('2em') # verticlal align formula with input
            st.markdown(f"$${var.latex} = {var.value:.3f} \ {var.unit}$$")
          
def variables_three_columns(var, display_formula=False, emoji="1️⃣"):
    col1, col2, col3 = st.columns([1,3,8])
    with col1:
        st.header(emoji)
    with col2:
        new_value = st.number_input(var.name, value=var.value, step=0.001, format="%.3f")
        var.value = new_value  # Update the variable's value
    with col3:
        if display_formula and var.formula:
            spacer('2em') # verticlal align formula with input
            st.markdown(f"$${var.formula} = {var.value:.3f} \ {var.unit}$$")
        else:
            spacer('2em') # verticlal align formula with input
            st.markdown(f"$${var.latex} = {var.value:.3f} \ {var.unit}$$")

def emoji_header(emoji, text):
    col1, col2 = st.columns([1,8])
    with col1:
        st.header(emoji)
    with col2:
        st.header(text)    

def display_generic_table(data):
    # Assume the first row of data contains all the keys we need for headers
    headers = data[0].keys()
    header_row = "| " + " | ".join(headers) + " |\n"
    separator_row = "|---" * len(headers) + "|\n"

    # Create the data rows
    data_rows = "".join(
        "| " + " | ".join(str(item[key]) for key in headers) + " |\n" for item in data
    )

    # Combine all the rows into a single table string
    table = header_row + separator_row + data_rows
    return table
