import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math
# from main import S

base_image = "./modules/draw/base_image.png"
svg_lines = "./modules/draw/svg_full_canvas.svg"

# st.image(base_image)

class Line:
    def __init__(self, start, end, real_length_m, line_color='white', line_width=2):
        self.start_x, self.start_y = start
        self.end_x, self.end_y = end
        self.real_length_m = real_length_m
        self.line_color = line_color
        self.line_width = line_width
        self.pixel_length = self.calculate_pixel_length()
        self.conversion_factor = self.calculate_conversion_factor()

    def calculate_pixel_length(self):
        return math.sqrt((self.end_x - self.start_x) ** 2 + (self.end_y - self.start_y) ** 2)

    def calculate_conversion_factor(self):
        return self.real_length_m / self.pixel_length if self.pixel_length else None

    def draw(self, draw):
        draw.line((self.start_x, self.start_y, self.end_x, self.end_y), fill=self.line_color, width=self.line_width)
        self.annotate_length(draw)

    def annotate_length(self, draw):
        text = f"{self.pixel_length}px / {self.real_length_m:.3f}m"
        midpoint = self.midpoint()
        text_position = (midpoint[0] + 10, midpoint[1] - 10)  # Adjust as needed
        draw.text(text_position, text, fill=self.line_color)

    def midpoint(self):
        return ((self.start_x + self.end_x) / 2, (self.start_y + self.end_y) / 2)


def draw_measurements_on_image(image_path, lines):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        for line in lines:
            line.draw(draw)
        st.image(img)

def draw_measurements_on_image(image_path, lines):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        for line in lines:
            line.draw(draw)
        st.image(img)

# Assume you have a list of lines with known real-world lengths
measurement_lines = [
    Line(start=(339, 222), end=(339, 281), real_length_m=0.340, line_color='red', line_width=2),
    # Line(start=(150, 250), end=(150, 450), real_length_m=3.5, line_color='red', line_width=2),
]

draw_measurements_on_image(base_image, measurement_lines)
