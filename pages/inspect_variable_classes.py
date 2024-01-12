import streamlit as st
import os
import re

def inspect_pages_variables():
    directories = ['./pages/', './']  # Directories to search for Python files
    variable_pattern = re.compile(r'\bVariable\(')

    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith('.py'):
                st.subheader(f"Variables in {filename}")
                with open(directory + filename, 'r') as file:
                    source = file.readlines()

                    # Collect lines that contain Variable instances
                    variable_lines = [line.strip() for line in source if variable_pattern.search(line)]

                    if variable_lines:
                        # Display all collected lines in a single code block
                        st.code("\n".join(variable_lines), language='python')
                    else:
                        st.write("No `Variable` instances found.")

def main():
    st.title("Session State Management")
    inspect_pages_variables()
    # ... (additional UI components or logic)

if __name__ == "__main__":
    main()
