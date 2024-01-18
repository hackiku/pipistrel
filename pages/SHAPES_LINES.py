### ./pages/SHAPES_LINES.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import svg2paths, parse_path
from modules.draw.draw import draw_measurements_on_image, parse_svg_for_lines

def extract_lines_from_svg(svg_file_path):
    paths, attributes = svg2paths(svg_file_path)
    lines = []

    for path in paths:
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            lines.append((start, end))

    return lines

def draw_lines_and_display_lengths(image_path, lines, conversion_factor):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=22)

    for line in lines:
        start, end = line
        # Use the SVG coordinates directly for the line drawing
        start_pixels = (start[0], start[1])
        end_pixels = (end[0], end[1])

        # Draw the line on the image
        draw.line([start_pixels, end_pixels], fill='red', width=3)

        # Calculate the length of the line in meters
        length_pixels = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        length_meters = length_pixels * conversion_factor

        # Find the midpoint for the text label using the SVG coordinates
        midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        length_text = f"{length_meters:.2f}m"

        # Display the length of the line on the image using the SVG's coordinate system
        draw.text(midpoint, length_text, fill='blue', font=font)

    return img



def calculate_polygon_area(vertices):
    # Initialize area
    area = 0.0
    # Calculate the area using the shoelace formula
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)  # Next vertex index
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area


def main():
    st.subheader("Wing area")

    base_image = "./modules/draw/drawing.png"
    svg_file_path = './modules/draw/s20.svg'

    # Get conversion factor from draw.py
    _, conversion_factor = parse_svg_for_lines(svg_file_path)

    if conversion_factor == 0:
        st.error("Conversion factor is zero, check your SVG lines and units.")
        st.stop()

    # Extract lines from SVG
    lines = extract_lines_from_svg(svg_file_path)

    # Draw lines and display lengths
    img = draw_lines_and_display_lengths(base_image, lines, conversion_factor)

    # Display the image with drawn lines and lengths
    st.image(img, caption='Wing with line lengths displayed')

    st.code(f"Conversion factor: {conversion_factor:.6f}")

if __name__ == "__main__":
    main()
