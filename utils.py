# utils.py
import streamlit as st
from variables_manager import get_variable_value, get_variable_props

def spacer(height='2em'):
    """Inserts vertical space in the layout."""
    spacer_html = f'<div style="margin: {height};"></div>'
    st.markdown(spacer_html, unsafe_allow_html=True)

# TODO create 2-col variable
# def input_latex_columns(latex=False):
#     col1, col2 = st.columns([2,3])
#     with col1:
    
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

def emoji_header(emoji, text, latex=None):
    col1, col2, col3 = st.columns([1,4,5])
    with col1:
        st.subheader(emoji)
    with col2:
        st.subheader(text)   
    with col3:
        st.latex(latex)

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


def final_value_input_oneline(title, value, success_message, warning_message, icon_success="✅", icon_warning="⚠️"):
    session_key = f"value_{title}"  # Create a unique session key based on the title
    if session_key not in st.session_state:
        st.session_state[session_key] = value  # Initialize session state with the default value
    
    col1, col2, col3, col4 = st.columns([1, 2, 3, 3])  # Adjust the width ratio as needed
    
    with col1:
        spacer('2em')
        if st.button("🔄", key=f"reset_{title}"):  # Ensure a unique key by using title
            st.session_state[session_key] = value  # Reset the session state value
            st.session_state[f"status_{title}"] = 'reset'  # Track the reset status separately in session state
        # Display current status
        current_status = st.session_state.get(f"status_{title}", 'default')
    
    with col2:
        # Use session state for number_input value
        user_input = st.number_input(title, value=st.session_state[session_key], format="%.3f", key=f"num_input_{title}")
        st.session_state[session_key] = user_input  # Update session state with new input
    
    with col3:
        if user_input == value:
            spacer('1em')
            st.success(f"{success_message.format(user_input)}", icon=icon_success)
            st.session_state[f"status_{title}"] = 'default'  # Update status in session state
        else:
            spacer('1em')
            st.warning(f"{warning_message.format(user_input)}", icon=icon_warning)
            st.session_state[f"status_{title}"] = 'changed'  # Update status in session state
    
    with col4:
        spacer('2em')
        st.text(current_status)
    
    return user_input

'''
def final_value_input(title, value, success_message, warning_message, icon_success="✅", icon_warning="⚠️"):
    col1, col2, col3, col4 = st.columns([1, 3, 3, 3])  # Adjust the width ratio as needed
    default_value = value
    with col1:
        st.write("Reset")
        if st.button("⏮️", key=f"reset_{title}"):  # Ensure a unique key by using title
            value = default_value  # Reset the value
            status = 'reset'
        else:
            status = 'default'
    with col2:
        user_input = st.number_input(title, value=value, format="%.3f")
    with col3:
        if user_input == value:
            spacer('1em')
            st.success(f"{success_message.format(value)}", icon=icon_success)
        else:
            spacer('1em')
            st.warning(f"{warning_message.format(user_input)}", icon=icon_warning)
            status = f'changed from = {default_value:.5f}'
            value = user_input  # Update the value if needed
    with col4:
        spacer('2em')
        st.text(status)
    return value, status
'''