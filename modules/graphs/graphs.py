# ./modules/graphs/graphs.py

import streamlit as st
from PIL import Image, ImageDraw, ImageOps

graph_paths = {
    'Re': './modules/graphs/Re_graph.png',
    'K_wing': './modules/graphs/K_wing_graph.png',
    'K_fuselage': './modules/graphs/K_fuselage_graph.png',
    's_fuselage': './modules/graphs/s_fuselage_graph.png'
}

# def draw_full_grid(img, grid_spacing, color="blue"):
#     width, height = img.size
#     draw = ImageDraw.Draw(img)
#     for x in range(0, width, grid_spacing):
#         draw.line((x, 0, x, height), fill=color, width=1)
#     for y in range(0, height, grid_spacing):
#         draw.line((0, y, width, y), fill=color, width=1)


def draw_grid(img, grid_spacing, vertical_line_x, horizontal_line_y, color="blue"):
    width, height = img.size
    draw = ImageDraw.Draw(img)

    # Calculate the number of lines to draw on each side of the origin
    num_lines = 10  # for a 10x10 grid on each quadrant

    # Draw vertical lines starting from the origin
    for i in range(-num_lines, num_lines + 1):
        x = vertical_line_x + i * grid_spacing
        line_width = 2 if i % 5 == 0 else 1  # Make every fifth line thicker
        if 0 <= x < width:  # Ensure the line is within the image bounds
            draw.line((x, 0, x, height), fill=color, width=line_width)

    # Draw horizontal lines starting from the origin
    for i in range(-num_lines, num_lines + 1):
        y = horizontal_line_y + i * grid_spacing
        line_width = 2 if i % 5 == 0 else 1  # Make every fifth line thicker
        if 0 <= y < height:  # Ensure the line is within the image bounds
            draw.line((0, y, width, y), fill=color, width=line_width)

def draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y, grid_spacing, invert_colors):
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')

            if grid_spacing > 0:
                draw_grid(img, grid_spacing, cross_position_x, cross_position_y)

            draw = ImageDraw.Draw(img)
            width, height = img.size

            # Draw red cross lines
            draw.line((0, cross_position_y, width, cross_position_y), fill="red", width=2)
            draw.line((cross_position_x, 0, cross_position_x, height), fill="red", width=2)

            if invert_colors == "Black":
                img = ImageOps.invert(img)

            return img
    except FileNotFoundError:
        st.error(f"The image {image_path} was not found.")
        return None


def draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y, grid_spacing, invert_colors):
    try:
        with Image.open(image_path) as img:

            if grid_spacing > 0:
                draw_grid(img, grid_spacing, cross_position_x, cross_position_y)

            
            draw = ImageDraw.Draw(img)
            width, height = img.size

            draw.line((0, cross_position_y, width, cross_position_y), fill="red", width=3)
            draw.line((cross_position_x, 0, cross_position_x, height), fill="red", width=3)

            if invert_colors == "Black":
                img = ImageOps.invert(img.convert('RGB'))

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

                col1, col2 = st.columns([3,1])
                with col1:
                    cross_position_x = st.slider('X position (left to right)', 0, width, default_cross_x, on_change=None)
                    cross_position_y = st.slider('Y position (top to bottom)', 0, height, default_cross_y, on_change=None)
                with col2:
                    show_grid = st.radio('Grid with sizing', ['Show', 'Hide'], index=1, horizontal=True)
                    grid_spacing = st.slider('Grid spacing', 2, 50, 25, label_visibility="collapsed")
                    invert_colors = st.radio('Invert colors', ['White', 'Black'], index=0, horizontal=True, label_visibility="collapsed")

                grid_spacing = grid_spacing if show_grid == 'Show' else 0
                modified_img = draw_red_cross_on_graph(image_path, cross_position_x, cross_position_y, grid_spacing, invert_colors)
                if modified_img:
                    st.image(modified_img, caption='Slide x to find your value → Slide y to match the curve → Read value on y axis', use_column_width=True)
        except FileNotFoundError:
            st.error(f"The image {image_path} was not found.")
    else:
        st.error(f"No graph found for the key '{graph_key}'.")
