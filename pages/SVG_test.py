import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/base_image.png"
svg_lines = "./modules/draw/morelines.svg"

def parse_svg_for_lines(svg_file):
    paths, attributes = svg2paths(svg_file)
    lines = []

    for path in paths:
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            real_length_m = abs(line.length())
            line_info = {'start': start, 'end': end, 'real_length_m': real_length_m}
            lines.append(line_info)
            st.code(line_info)  # Log the parsed line information

    return lines

def draw_measurements_on_image(image_path, lines):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=24)

        for line in lines:
            start, end = line['start'], line['end']
            real_length_m = line['real_length_m']
            draw.line([start, end], fill='red', width=3)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m"
            draw.text(midpoint, text, fill='red', font=font)
        st.image(img)

def main():
    st.title("SVG Line Measurements")
    lines = parse_svg_for_lines(svg_lines)
    draw_measurements_on_image(base_image, lines)

    st.image(svg_lines)
    
if __name__ == "__main__":
    main()