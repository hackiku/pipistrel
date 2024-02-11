# ./modules/graphs/graphs.py

# graph_key = st.selectbox("Select a graph to display", options=['Re', 'K_wing', 'K_fuselage'])

import streamlit as st
from PIL import Image, ImageDraw

graph_paths = {
    'Re': './modules/graphs/Re_graph.png',
    'K_wing': './modules/graphs/K_wing_graph.png',
    'K_fuselage': './modules/graphs/K_fuselage_graph.png',
    's_fuselage': './modules/graphs/s_fuselage_graph.png'
}

def draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y):
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            width, height = img.size

            draw.line((0, cross_position_y, width, cross_position_y), fill="red", width=2)
            draw.line((cross_position_x, 0, cross_position_x, height), fill="red", width=2)

            return img
    except FileNotFoundError:
        st.error(f"The image {image_path} was not found.")
        return None

def readout_graph(graph_key, default_cross_x=None, default_cross_y=None):
    if graph_key in graph_paths:
        image_path = graph_paths[graph_key]
        try:
            with Image.open(image_path) as img:
                width, height = img.size

                # Default positions for sliders
                default_cross_x = default_cross_x if default_cross_x is not None else width // 2
                default_cross_y = default_cross_y if default_cross_y is not None else height // 2

                cross_position_x = st.slider('X position (left to right)', 0, width, default_cross_x)
                cross_position_y = st.slider('Y position (top to bottom)', 0, height, default_cross_y)

                modified_img = draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y)
                if modified_img:
                    st.image(modified_img, caption='Modified Graph with Red Cross')
        except FileNotFoundError:
            st.error(f"The image {image_path} was not found.")
    else:
        st.error(f"No graph found for the key '{graph_key}'.")
