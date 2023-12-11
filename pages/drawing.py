import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math

class Line:
    def __init__(self, start, end, line_color, line_width=3, label=None):
        self.start = start
        self.end = end
        self.line_color = line_color
        self.line_width = line_width
        self.label = label

    def draw(self, draw):
        draw.line((self.start, self.end), fill=self.line_color, width=self.line_width)
        mid_x, mid_y = self.midpoint()
        if self.label:
            draw_text(draw, self.label, (mid_x, mid_y - 10), text_color=self.line_color)
        return math.sqrt((self.end[0] - self.start[0]) ** 2 + (self.end[1] - self.start[1]) ** 2)

    def midpoint(self):
        mid_x = (self.start[0] + self.end[0]) // 2
        mid_y = (self.start[1] + self.end[1]) // 2
        return (mid_x, mid_y)

def draw_text(draw, text, position, text_color="white"):
    font = ImageFont.load_default()
    draw.text(position, text, fill=text_color, font=font)

class Trapezoid:
    def __init__(self, top_left, top_right, bottom_right, bottom_left, color="red", line_width=2):
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.color = color
        self.line_width = line_width

    def draw(self, draw):
        # Draw the four sides of the trapezoid
        draw.line([self.top_left, self.top_right, self.bottom_right, self.bottom_left, self.top_left], 
                  fill=self.color, width=self.line_width)



img = Image.open("./assets/wing_black.jpg")
width, height = img.size
draw = ImageDraw.Draw(img)

# Initialize lines
original_line = Line((258, 25), (258, 336), line_color="green", label="Line 1")
line_fuselage = Line((150, 160), (150, 600), line_color="orange", label="Line 2")
line_powerplant = Line((388, 328), (616, 328), line_color="blue", label="Line 3")

# Streamlit UI for selecting and modifying specific lines
selected_line = st.selectbox("Select Line to Modify", ["Original Line", "Line Fuselage", "Line Powerplant"])

# Setting default values for number_input
if selected_line == "Original Line":
    default_values = (258, 25, 258, 336)
elif selected_line == "Line Fuselage":
    default_values = (139, 348, 139, 431)
elif selected_line == "Line Powerplant":
    default_values = (388, 328, 616, 328)

col1, col2, col3, col4 = st.columns(4)
with col1:
    start_x = st.number_input('Start X', value=default_values[0], max_value=width)
with col2:
    start_y = st.number_input('Start Y', value=default_values[1], max_value=height)
with col3:
    end_x = st.number_input('End X', value=default_values[2], max_value=width)
with col4:
    end_y = st.number_input('End Y', value=default_values[3], max_value=height)

# Update line position based on selection
if selected_line == "Original Line":
    original_line = Line((start_x, start_y), (end_x, end_y), line_color="green", label="Line 1")
elif selected_line == "Line Fuselage":
    line_fuselage = Line((start_x, start_y), (end_x, end_y), line_color="orange", label="Line 2")
elif selected_line == "Line Powerplant":
    line_powerplant = Line((start_x, start_y), (end_x, end_y), line_color="blue", label="Line 3")

# Drawing lines
line_length_pixels = original_line.draw(draw)
line_fuselage.draw(draw)
line_powerplant.draw(draw)

# Conversion factor calculations
length_original_meters = 4.855  # The original length in meters
conversion_factor = line_length_pixels / length_original_meters
line_length_meters = line_length_pixels / conversion_factor


y1 = y2 = 26
x1 = 325 # top left
x2 = 380 # top right
y3 = y4 = 400 # bottom
x3 = 380
x4 = 309

top_left = (x1, y1)
top_right = (x2, y2)
bottom_right = (x3, y3)
bottom_left = (x4, y4)

# Create the trapezoid object
wing_trapezoid = Trapezoid(top_left, top_right, bottom_right, bottom_left, color="red")

# Draw the trapezoid on the image
wing_trapezoid.draw(draw)



# Display the image
st.image(img)