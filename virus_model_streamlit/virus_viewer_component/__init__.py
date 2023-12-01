import os
import streamlit.components.v1 as components

def virus_viewer():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(current_dir, 'frontend', 'index.html')

    with open(html_file, 'r') as file:
        html_content = file.read()

    components.html(html_content, height=600)
