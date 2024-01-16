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
            real_length_m = line['length_pixels'] * conversion_factor  # Use the conversion factor to calculate the real length
            draw.line([start, end], fill='red', width=5)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m"
            draw.text(midpoint, text, fill='red', font=font)
        return img

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
if __name__ == "__main__":
    main()