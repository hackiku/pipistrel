import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math

class Line:
    # Default positions as a class variable
    default_positions = [100, 200, 300, 400]

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

    def annotate_length(self, draw, meter_length=None):
        pixel_length = self.calculate_length()
        text = f"{pixel_length}px"
        if meter_length is not None:
            text += f"\n {meter_length:.3f}m"

        midpoint = self.midpoint()
        offset = (20, 10)
        text_position = (midpoint[0] + offset[0], midpoint[1] + offset[1])
        draw_text(draw, text, text_position, text_color=self.line_color)

    def calculate_length(self):
        # Calculate the length of the line
        return int(math.sqrt((self.end_x - self.start_x) ** 2 + (self.end_y - self.start_y) ** 2))

    def midpoint(self):
        # Calculate the midpoint of the line for annotation purposes
        return ((self.start_x + self.end_x) // 2, (self.start_y + self.end_y) // 2)

lines = {
    'Wing Measurement': Line([357, 262, 914, 262], line_color="green", line_width=1),
    'Tail Measurement': Line([365, 449, 365, 848], line_color="red", line_width=1),
    'Body Measurement': Line([228, 60, 364, 60], line_color="yellow", line_width=1),
    'Centerline': Line([296, 112, 296, 932], line_color="orange", line_width=1),
    'Elevator Width': Line([168, 960, 425, 960], line_color="yellow", line_width=1),
    'Elevator Length': Line([100, 847, 100, 934], line_color="green", line_width=1),
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

def draw_text(draw, text, position, text_color='white', font_size=40):
    # font = ImageFont.truetype("arial.ttf", font_size)
    font = ImageFont.load_default()
    draw.text(position, text, fill=text_color, font=font)

def convert_px_to_m(pixel_length):
    wing_length_original = 4.855
    tail_length_original = 3.210
    fuselage_length_original = 1.100
    return wing_length_original / pixel_length

img_path = "./assets/wing_black_horizontal.png"
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

# define canvas
pixel_canvas_width, pixel_canvas_height = img.size
# meter_canvas_width = pixel_canvas_width * conversion_factor
# meter_canvas_height = pixel_canvas_height * conversion_factor

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

wing_pixel_length = lines['Wing Measurement'].calculate_length()
conversion_factor = convert_px_to_m(wing_pixel_length)

# Redraw the lines on the image
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

for line_key, line in lines.items():
    pixel_length = line.calculate_length()
    meter_length = pixel_length * conversion_factor
    line.annotate_length(draw, meter_length)

draw_all_lines(draw, lines)

canvas_info_position = (pixel_canvas_width - int(0.2 * pixel_canvas_width), pixel_canvas_height - int(0.2 * pixel_canvas_height))
draw_text(draw, f"Pixel canvas = {pixel_canvas_width}x{pixel_canvas_height}px", canvas_info_position)
# draw_text(draw, f"Meter canvas = {meter_canvas_width:.2f} x {meter_canvas_height:.2f} m", (canvas_info_position[0], canvas_info_position[1] + 30))
draw_text(draw, f"Conversion factor: {conversion_factor:.4f} m/px", (canvas_info_position[0], canvas_info_position[1] + 60))
draw_text(draw, f"Conversion factor: {1/conversion_factor:.4f} px/m", (canvas_info_position[0], canvas_info_position[1] + 90))
# Display the updated image in the Streamlit app
st.image(img)