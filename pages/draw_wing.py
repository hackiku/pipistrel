### ./pages/draw_wing.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from modules.draw.draw import draw_measurements_on_image, parse_svg_for_lines


def draw_trapezoid(image_path, lines, conversion_factor):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=22)

        for line in lines:
            start, end = line['start'], line['end']
            real_length_m = line['length_pixels'] * conversion_factor
            draw.line([start, end], fill='red', width=5)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m"
            draw.text(midpoint, text, fill='red', font=font)
            st.code(line)

        # Crop the image to the bottom 1300px height
        width, height = img.size
        img = img.crop((0, height - 1500, width, height))

        return img
    
def calculate_trapezoid_area(vertices, conversion_factor):
    # Order the vertices: top_left, top_right, bottom_right, bottom_left
    top_left, top_right, bottom_right, bottom_left = vertices

    # Calculate the lengths of the top and bottom bases
    top_base_length = ((top_right[0] - top_left[0])**2 + (top_right[1] - top_left[1])**2)**0.5
    bottom_base_length = ((bottom_right[0] - bottom_left[0])**2 + (bottom_right[1] - bottom_left[1])**2)**0.5

    # Calculate the height using the distance between midpoints of the bases
    midpoint_top_base = ((top_left[0] + top_right[0]) / 2, (top_left[1] + top_right[1]) / 2)
    midpoint_bottom_base = (bottom_left[0] + bottom_right[0])


def main():
    st.subheader("Wing area")
    base_image = "./modules/draw/drawing.png"
    svg_lines = "./modules/draw/wing_draw.svg"
    reference_svg_lines = "./modules/draw/lines.svg"  # Add path to your reference lines SVG file

    _, conversion_factor = parse_svg_for_lines(reference_svg_lines)

    # Parse the lines from the actual SVG file
    lines, _ = parse_svg_for_lines(svg_lines)

    # Draw the trapezoid with the real conversion factor
    img = draw_trapezoid(base_image, lines, conversion_factor)

    st.image(img)
    st.code(f"conversion factor: {conversion_factor}")
    
    # l0 = Variable("Tip Chord Length", trapezoid.l_0_px * conversion_factor, "l_{0}", "m")
    # l1 = Variable("Root Chord Length", trapezoid.l_1_px * conversion_factor, "l_{1}", "m")
    # b = Variable("Wingspan", half_wingspan_meters*2, "b", "m")  # Use a Variable instance for the wingspan
    
    st.latex(f"S_{{20}} = \\frac{{{l0.latex} + {l1.latex}}}{2} \\cdot \\frac{{{b.latex}}}{2} = \\frac{{{l0.value:.3f} + {l1.value:.3f}}}{2} \\cdot \\frac{{{b.value:.3f}}}{2} = {trapezoid_area:.3f} \\, \\text{{m}}^2")
    st.latex(f"S = S_{{20}} \\cdot 2 = {trapezoid_area*2:.3f} \\, \\text{{m}}^2")

    calculate_trapezoid_area()
if __name__ == "__main__":
    main()