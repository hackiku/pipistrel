import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math

class Line:
    # Default positions as a class variable
    default_positions = [360, 262, 920, 262]

    def __init__(self, positions=None, line_color='white', line_width=2):
        # If no specific positions are provided, use the default ones
        if positions is None:
            positions = Line.default_positions
        self.start_x, self.start_y, self.end_x, self.end_y = positions
        self.line_color = line_color
        self.line_width = line_width

    def draw(self, draw):
        # Draw the line on the image
        draw.line((self.start_x, self.start_y, self.end_x, self.end_y), fill=self.line_color, width=self.line_width)
        self.annotate_length(draw)

    def annotate_length(self, draw):
        # Annotate the length of the line on the image
        length = self.calculate_length()
        midpoint = self.midpoint()
        offset = (10, -10)
        text_position = (midpoint[0] + offset[0], midpoint[1] + offset[1])
        draw_text(draw, f"{length}px", text_position, text_color=self.line_color)

    def calculate_length(self):
        # Calculate the length of the line
        return int(math.sqrt((self.end_x - self.start_x) ** 2 + (self.end_y - self.start_y) ** 2))

    def midpoint(self):
        # Calculate the midpoint of the line for annotation purposes
        return ((self.start_x + self.end_x) // 2, (self.start_y + self.end_y) // 2)

lines = {
    'Wing Measurement': Line([358, 262, 914, 262], line_color="green", line_width=1),
    'Tail Measurement': Line([365, 449, 365, 848], line_color="green", line_width=1),
    'Body Measurement': Line([228, 60, 364, 60], line_color="blue", line_width=1),
    'Centerline': Line([296, 112, 296, 932], line_color="orange", line_width=1)
}

def update_line_positions(line, start_x, start_y, end_x, end_y):
    line.start_x = start_x
    line.start_y = start_y
    line.end_x = end_x
    line.end_y = end_y

# Draw all lines on the image
def draw_all_lines(draw, lines):
    for line in lines.values():
        line.draw(draw)

def draw_text(draw, text, position, text_color='white', font_size=20):
    # font = ImageFont.truetype("arial.ttf", font_size)
    font = ImageFont.load_default()
    draw.text(position, text, fill=text_color, font=font)

def convert_px_to_m():
    wing_length_original = 4.855
    tail_length_original = 3.210
    fuselage_length_original = 1.100
    # conversion factors here
    
    return conversion_factor


img_path = "./assets/wing_black_horizontal.png"
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

# define canvas
pixel_canvas_width, pixel_canvas_height = img.size
meter_canvas_width = 4.855
meter_canvas_height = meter_canvas_width * (pixel_canvas_height / pixel_canvas_width)  # Preserving aspect ratio


# Column layout for the line position controls
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    selected_line_key = st.selectbox('Select Line to Modify', list(lines.keys()))
    selected_line = lines[selected_line_key]
with col2:
    start_x = st.number_input('Start X', value=selected_line.start_x, max_value=pixel_canvas_width, step=1)
with col3:
    start_y = st.number_input('Start Y', value=selected_line.start_y, max_value=pixel_canvas_height, step=1)
with col4:
    end_x = st.number_input('End X', value=selected_line.end_x, max_value=pixel_canvas_width, step=1)
with col5:
    end_y = st.number_input('End Y', value=selected_line.end_y, max_value=pixel_canvas_height, step=1)

# Update the selected line with the new positions
update_line_positions(selected_line, start_x, start_y, end_x, end_y)

# Redraw the lines on the image
img = Image.open(img_path)
draw = ImageDraw.Draw(img)
draw_all_lines(draw, lines)

# Display the updated image in the Streamlit app
st.image(img)