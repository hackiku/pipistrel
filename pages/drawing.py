import streamlit as st
from PIL import Image, ImageDraw

# Load your image
img = Image.open("./assets/wing_black.jpg")

# Get the dimensions of the image
width, height = img.size

# Use Streamlit sliders to select the position of the line
start_x = st.slider('Start X position', 0, width, 787)
start_y = st.slider('Start Y position', 0, height, 26)
end_x = st.slider('End X position', 0, width, 258)
end_y = st.slider('End Y position', 0, height, 350)

# Draw a line on the image using the selected positions
draw = ImageDraw.Draw(img)
draw.line((start_x, start_y, end_x, end_y), fill="red", width=3)

# Display the image
st.image(img)
