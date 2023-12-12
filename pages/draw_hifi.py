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

    # Draw the line on the image

    def draw(self, draw):
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
    'Wing Measurement': Line([356, 360, 915, 360], line_color="green", line_width=1),
    'Tail Measurement': Line([365, 449, 365, 848], line_color="red", line_width=1),
    'Fuselage Measurement': Line([228, 60, 364, 60], line_color="yellow", line_width=1),
    'Cabin Measurement': Line([236, 120, 356, 120], line_color="yellow", line_width=1),
    'Elevator Width': Line([168, 960, 425, 960], line_color="yellow", line_width=1),
    'Elevator Length': Line([100, 848, 100, 934], line_color="green", line_width=1),
    # 'Centerline': Line([296, 112, 296, 932], line_color="orange", line_width=1),
}

class Trapezoid:
    def __init__(self, l_0, l_1, x_root, x_tip, y_root, y_tip, line_color='red', line_width=2):
        self.l_0 = l_0
        self.l_1 = l_1
        self.x_root = x_root
        self.x_tip = x_tip
        self.y_root = y_root
        self.y_tip = y_tip
        self.line_color = line_color
        self.line_width = line_width

    def draw(self, draw):
        # Calculate corner points
        top_left = (self.x_root, self.y_root - self.l_0 / 2)
        top_right = (self.x_tip, self.y_root - self.l_0 / 2)
        bottom_left = (self.x_root, self.y_root + self.l_0 / 2)
        bottom_right = (self.x_tip, self.y_tip + self.l_1 / 2)

        # Draw the trapezoid
        draw.line([top_left, bottom_left], fill=self.line_color, width=self.line_width)
        draw.line([bottom_left, bottom_right], fill=self.line_color, width=self.line_width)
        draw.line([bottom_right, top_right], fill=self.line_color, width=self.line_width)
        draw.line([top_right, top_left], fill=self.line_color, width=self.line_width)

default_trapezoid_values = [100, 20, 500, 600, 400, 450]
trapezoid = Trapezoid(*default_trapezoid_values)

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

known_lengths = {
    'Wing Measurement': 4.855,
    'Tail Measurement': 3.210,
    'Fuselage Measurement': 1.100,
    'Cabin Measurement': 1.000,
    'Elevator Width': 2.175,
    'Elevator Length': 0.738,
}

def convert_px_to_m(lines):
    total_weighted_conversion = 0
    total_pixel_length = 0

    for line_key, real_length in known_lengths.items():
        if line_key in lines:
            pixel_length = lines[line_key].calculate_length()
            if pixel_length > 0:
                conversion_factor = real_length / pixel_length
                # Weight the conversion factor by the pixel length of the line
                total_weighted_conversion += conversion_factor * pixel_length
                total_pixel_length += pixel_length

    if total_pixel_length > 0:
        # Calculate the weighted average conversion factor
        return total_weighted_conversion / total_pixel_length
    else:
        return None

    # if conversion_factors:
    #    return sum(conversion_factors) / len(conversion_factors)
    # else:
    #    return None

img_path = "./assets/wing_black_horizontal.png"
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

# define canvas
pixel_canvas_width, pixel_canvas_height = img.size

# STATE
for line_key in lines.keys():
    if line_key not in st.session_state:
        line = lines[line_key]
        st.session_state[line_key] = [line.start_x, line.start_y, line.end_x, line.end_y]

with st.expander("Measurements"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        selected_line_key = st.selectbox('Select Line to Modify', list(lines.keys()))
        # selected_line = lines[selected_line_key]
    with col2:
        st.session_state[selected_line_key][0] = st.number_input('Start X', value=st.session_state[selected_line_key][0], max_value=pixel_canvas_width, step=1)
    with col3:
        st.session_state[selected_line_key][1] = st.number_input('Start Y', value=st.session_state[selected_line_key][1], max_value=pixel_canvas_height, step=1)
    with col4:
        st.session_state[selected_line_key][2] = st.number_input('End X', value=st.session_state[selected_line_key][2], max_value=pixel_canvas_width, step=1)
    with col5:
        st.session_state[selected_line_key][3] = st.number_input('End Y', value=st.session_state[selected_line_key][3], max_value=pixel_canvas_height, step=1)

col1, col2, col3 = st.columns(3)
with col1:
    trapezoid.l_0 = st.number_input('Root Length (l_0)', value=trapezoid.l_0, step=10)
with col2:
    trapezoid.x_root = st.number_input('Root X Position (x_root)', value=trapezoid.x_root, step=10)
with col3:
    trapezoid.y_root = st.number_input('Root Y Position (y_root)', value=trapezoid.y_root, step=10)

col4, col5, col6 = st.columns(3)
with col4:
    trapezoid.l_1 = st.number_input('Tip Length (l_1)', value=trapezoid.l_1, step=10)
with col5:
    trapezoid.x_tip = st.number_input('Tip X Position (x_tip)', value=trapezoid.x_tip, step=10)
with col6:
    trapezoid.y_tip = st.number_input('Tip Y Position (y_tip)', value=trapezoid.y_tip, step=10)

# Update the selected line with the new positions
selected_line = lines[selected_line_key]
selected_line.start_x, selected_line.start_y, selected_line.end_x, selected_line.end_y = st.session_state[selected_line_key]

trapezoid.draw(draw)

for key, line in lines.items():
    if key in st.session_state:
        line.start_x, line.start_y, line.end_x, line.end_y = st.session_state[key]

# update_line_positions(selected_line, start_x, start_y, end_x, end_y)

conversion_factor = convert_px_to_m(lines)

# Redraw the lines on the image
img = Image.open(img_path)
draw = ImageDraw.Draw(img)

for line_key, line in lines.items():
    pixel_length = line.calculate_length()
    meter_length = pixel_length * conversion_factor
    line.annotate_length(draw, meter_length)

trapezoid.draw(draw)
draw_all_lines(draw, lines)

canvas_info_position = (pixel_canvas_width - int(0.2 * pixel_canvas_width), pixel_canvas_height - int(0.2 * pixel_canvas_height))
draw_text(draw, f"Pixel canvas = {pixel_canvas_width}x{pixel_canvas_height}px", canvas_info_position)
# draw_text(draw, f"Meter canvas = {meter_canvas_width:.2f} x {meter_canvas_height:.2f} m", (canvas_info_position[0], canvas_info_position[1] + 30))
draw_text(draw, f"Conversion factor: {conversion_factor:.4f} m/px", (canvas_info_position[0], canvas_info_position[1] + 60))
draw_text(draw, f"Conversion factor: {1/conversion_factor:.4f} px/m", (canvas_info_position[0], canvas_info_position[1] + 90))
# Display the updated image in the Streamlit app

table_data = []
for line_key, line in lines.items():
    pixel_length = line.calculate_length()
    meter_length = pixel_length * conversion_factor
    actual_length = known_lengths.get(line_key, 0)
    error = abs(actual_length - meter_length) / actual_length * 100 if actual_length else 0
    table_data.append((line_key, pixel_length, meter_length, actual_length, error))

# Display the table in Streamlit
table_markdown = "| Measurement | Pixel Length | Calculated Length (m) | Actual Length (m) | Error (%) |\n"
table_markdown += "| ------------ | ------------- | ---------------------- | ------------------ | ---------- |\n"
for data in table_data:
    table_markdown += f"| {data[0]} | {data[1]:.2f}px | {data[2]:.3f}m | {data[3]:.3f}m | {data[4]:.2f}% |\n"

st.image(img)
st.markdown(table_markdown)