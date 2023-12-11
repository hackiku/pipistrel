import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math

def draw_line(draw, start, end, line_color="green", line_width=2):
    draw.line((start, end), fill=line_color, width=line_width)
    return math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)

def draw_text(draw, text, position, text_color="white"):
    # Use a default PIL font
    font = ImageFont.load_default()
    # Draw text without calculating its size
    draw.text(position, text, fill=text_color, font=font)


img = Image.open("./assets/wing_black.jpg")

width, height = img.size

coordinates = {
    "start_x": st.number_input('Start X position', min_value=0, max_value=width, value=258, step=1),
    "start_y": st.number_input('Start Y position', min_value=0, max_value=height, value=25, step=1),
    "end_x": st.number_input('End X position', min_value=0, max_value=width, value=258, step=1),
    "end_y": st.number_input('End Y position', min_value=0, max_value=height, value=354, step=1)
}

draw = ImageDraw.Draw(img)
line_length_pixels = draw_line(draw, (coordinates["start_x"], coordinates["start_y"]), (coordinates["end_x"], coordinates["end_y"]))

length_original = 4.855
# wing_measure = 3.290

conversion_factor = line_length_pixels / length_original

line_length_meters = line_length_pixels / conversion_factor

text_position = (50, 50)
draw_text(draw, "4850", text_position, text_color='red')

text_position = (400, 50)
draw_text(draw, f"{conversion_factor}", text_position)

# Midpoint of the line
mid_x = (coordinates["start_x"] + coordinates["end_x"]) // 2
mid_y = (coordinates["start_y"] + coordinates["end_y"]) // 2

draw_text(draw, f"Length = {line_length_meters:.3f} m", (mid_x, mid_y - 10))

# Display the image and line length
st.image(img)
st.write(f"Start Point: ({coordinates['start_x']}, {coordinates['start_y']})")
st.write(f"End Point: ({coordinates['end_x']}, {coordinates['end_y']})")
st.write(f"Line Length: {line_length_meters:.3f} m (in meters)")