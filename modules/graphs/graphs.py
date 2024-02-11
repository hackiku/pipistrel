# ./modules/graphs/graphs.py

import streamlit as st
from PIL import Image, ImageDraw

# Dictionary mapping graph identifiers to their file paths
graph_paths = {
    'Re': './modules/graphs/Re_graph.png',
    'K_wing': './modules/graphs/K_wing_graph.png',
    'K_fuselage': './modules/graphs/K_fuselage_graph.png',
    's_fuselage': './modules/graphs/s_fuselage_graph.png'
}

def draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y):
    """
    Load a graph image, draw a red cross over it at specified positions, and return the modified image.

    Parameters:
    - image_path: str, path to the original graph image.
    - cross_position_x: int, position of the cross along the x-axis.
    - cross_position_y: int, position of the cross along the y-axis.

    Returns:
    - An Image object with a red cross drawn over it.
    """
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)

            # Get image dimensions
            width, height = img.size

            # Draw two lines (a cross) over the image based on slider positions
            draw.line((0, cross_position_y, width, cross_position_y), fill="red", width=2)
            draw.line((cross_position_x, 0, cross_position_x, height), fill="red", width=2)

            return img
    except FileNotFoundError:
        st.error(f"The image {image_path} was not found.")
        return None

def readout_graph(graph_key):
    """
    Streamlit UI for loading a graph, adjusting cross position with sliders, and displaying the modified image.

    Parameters:
    - graph_key: str, key of the graph in the graph_paths dictionary.
    """
    if graph_key in graph_paths:
        image_path = graph_paths[graph_key]

        # Attempt to open the image to get its dimensions for slider max values
        try:
            with Image.open(image_path) as img:
                width, height = img.size

                # Sliders for adjusting the cross position
                cross_position_x = st.slider('Adjust cross X position', 0, width, width // 2)
                cross_position_y = st.slider('Adjust cross Y position', 0, height, height // 2)

                # Draw the cross on the graph based on slider positions
                modified_img = draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y)
                if modified_img:
                    # Display the modified image in Streamlit
                    st.image(modified_img, caption='Modified Graph with Red Cross')
        except FileNotFoundError:
            st.error(f"The image {image_path} was not found.")
    else:
        st.error(f"No graph found for the key '{graph_key}'.")
