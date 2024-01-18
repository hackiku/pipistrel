# Example usage in a Streamlit page
import streamlit as st
from modules.draw.draw import draw_lines_and_display_lengths

def show_wing_page():
    base_image_path = "./modules/draw/drawing.png"
    svg_file_path = './modules/draw/s20.svg'
    font_path = './assets/Roboto_Mono/static/RobotoMono-Regular.ttf'
    
    # Draw lines and get their lengths
    img, line_lengths = draw_lines_and_display_lengths(base_image_path, svg_file_path, font_path)

    # Display the image with lines and lengths
    st.image(img, caption='Wing with lines and measurements')

    # Display line lengths
    for length in line_lengths:
        st.write(f"Line length: {length:.2f}m")

if __name__ == "__main__":
    show_wing_page()

