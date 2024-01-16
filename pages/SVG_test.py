import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import math

# Path to the base image and SVG file
base_image = "./modules/draw/base_image.png"
svg_lines = "./modules/draw/measurement_lines.svg"
# st.image(svg_lines)

def parse_svg_for_lines(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    lines = []

    for element in root.iter():
        if element.tag.endswith('path'):
            d = element.attrib.get('d', '')
            if d.startswith('M') and 'L' in d:
                m, l = d[1:].split('L')
                start = tuple(map(float, m.split()))
                end = tuple(map(float, l.split()))
                real_length_m = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                lines.append({'start': start, 'end': end, 'real_length_m': real_length_m})
    return lines

def draw_measurements_on_image(image_path, lines):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=24)

        for line in lines:
            start, end = line['start'], line['end']
            real_length_m = line['real_length_m']
            draw.line([start, end], fill='red', width=2)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m"
            draw.text(midpoint, text, fill='red', font=font)
        st.image(img)

def main():
    st.title("SVG Line Measurements")
    lines = parse_svg_for_lines(svg_lines)
    draw_measurements_on_image(base_image, lines)

if __name__ == "__main__":
    main()
