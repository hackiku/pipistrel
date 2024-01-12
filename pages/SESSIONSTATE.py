### ./pages/sessionstate.py

import streamlit as st
import os
import inspect
from data import Variable

# Function to register a variable in the session state
def register_variable(var):
    if var.python in st.session_state:
        st.session_state[var.python].value = var.value
    else:
        st.session_state[var.python] = var

# Function to get a variable from the session state
def get_variable(name, default_value):
    return st.session_state.get(name, Variable(name, default_value)).value

# Function to inspect and display variables from all pages
def inspect_pages_variables():
    pages_dir = './pages/'
    for filename in os.listdir(pages_dir):
        if filename.endswith('.py'):
            st.header(f"Variables in {filename}")
            with open(pages_dir + filename, 'r') as file:
                source = file.read()
                # Inspect the source code for Variable definitions
                # (You might need a more complex parser for accurate results)
                for line in source.split('\n'):
                    if 'Variable(' in line:
                        st.code(line.strip())

# Main function for session state management
def main():
    st.title("Session State Management")
    
    # Display variables from all pages
    inspect_pages_variables()
    
    # ... (You can add more UI components or logic here as needed)

if __name__ == "__main__":
    main()
