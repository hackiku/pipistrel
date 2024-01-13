import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import math
# from main import S


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
    'Wing Measurement': Line([356, 260, 915, 260], line_color="green", line_width=1),
    'Tail Measurement': Line([342, 449, 342, 848], line_color="green", line_width=1),
    'Fuselage Measurement': Line([228, 60, 364, 60], line_color="green", line_width=1),
    'Cabin Measurement': Line([236, 115, 356, 115], line_color="green", line_width=1),
    'Elevator Width': Line([168, 960, 425, 960], line_color="green", line_width=1),
    'Elevator Length': Line([100, 848, 100, 934], line_color="green", line_width=1),
    # 'Centerline': Line([296, 112, 296, 932], line_color="orange", line_width=1),
}

class Trapezoid:
    def __init__(self, l_0_px, l_1_px, x_root, x_tip, y_root, y_tip, line_color='red', line_width=2):
        self.l_0_px = l_0_px  # Tip length
        self.l_1_px = l_1_px  # Root length
        self.x_root = x_root  # X position for the root line
        self.x_tip = x_tip  # X position for the tip line
        self.y_root = y_root  # Top y-coordinate for the root line
        self.y_tip = y_tip  # Top y-coordinate for the tip line
        self.line_color = line_color
        self.line_width = line_width

    def draw(self, draw):
        # Calculate corner points for the trapezoid
        top_root = (self.x_root, self.y_root)
        bottom_root = (self.x_root, self.y_root + self.l_1_px)
        top_tip = (self.x_tip, self.y_tip)
        bottom_tip = (self.x_tip, self.y_tip + self.l_0_px)

        # Draw the trapezoid
        draw.line([top_root, bottom_root], fill=self.line_color, width=self.line_width)  # Root line
        draw.line([bottom_root, bottom_tip], fill=self.line_color, width=self.line_width)  # Bottom line
        draw.line([bottom_tip, top_tip], fill=self.line_color, width=self.line_width)  # Tip line
        draw.line([top_tip, top_root], fill=self.line_color, width=self.line_width)  # Top line

    # box for lift coefficient over wing diagram
    def get_bounding_box(self):
        top_root = (self.x_root, self.y_root)
        bottom_root = (self.x_root, self.y_root + self.l_1_px)
        top_tip = (self.x_tip, self.y_tip)
        bottom_tip = (self.x_tip, self.y_tip + self.l_0_px)

        left = min(self.x_root, self.x_tip)
        right = max(self.x_root, self.x_tip)
        top = min(self.y_root, self.y_tip)
        bottom = max(self.y_root + self.l_1_px, self.y_tip + self.l_0_px)

        return (left, top, right, bottom)


# x root = 100: arbitrary, later uses average_x_root
default_trapezoid_values = [94, 121, 0, 899, 328, 356]
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

def draw_text(draw, text, position, text_color='white', font_size=16):
    # Load the custom font from the specified path
    font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', font_size)
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


# find center of 3x horizontal body lines
def calculate_average_center(lines, line_keys):
    midpoints = []
    for key in line_keys:
        line = lines[key]
        midpoints.append((line.start_x + line.end_x) // 2)
    # Calculate the average of the midpoints
    average_midpoint = sum(midpoints) // len(midpoints)
    return average_midpoint



def main():

    img_choice = st.radio("Image format", ["Black", "White"])
    if img_choice == "Black":
        img_path = "./assets/wing_black.png"
    else:
        img_path = "./assets/wing_white.png"

    img = Image.open(img_path)
    
    # define canvas
    pixel_canvas_width, pixel_canvas_height = img.size

    line_keys = ['Fuselage Measurement', 'Cabin Measurement', 'Elevator Width']
    average_x_root = calculate_average_center(lines, line_keys)
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
    
    #==================== TRAPEZOID ====================#
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text("dimensions")
        trapezoid.l_0_px = st.number_input('Tip Length (l_0_px)', value=trapezoid.l_0_px, step=1)
    with col2:
        st.text("vertical sides")
        trapezoid.x_root = st.number_input('Root X Position (x_root)', value=average_x_root, step=1)
    with col3:
        st.text("move up/down")
        trapezoid.y_root = st.number_input('Root Y Position (y_root)', value=trapezoid.y_root, step=1)

    col4, col5, col6 = st.columns(3)
    with col4:
        trapezoid.l_1_px = st.number_input('Root Length (l_1_px)', value=trapezoid.l_1_px, step=1)
    with col5:
        trapezoid.x_tip = st.number_input('Tip X Position (x_tip)', value=trapezoid.x_tip, step=1)
    with col6:
        trapezoid.y_tip = st.number_input('Tip Y Position (y_tip)', value=trapezoid.y_tip, step=1)

    # Update the selected line with the new positions
    selected_line = lines[selected_line_key]
    selected_line.start_x, selected_line.start_y, selected_line.end_x, selected_line.end_y = st.session_state[selected_line_key]

    for key, line in lines.items():
        if key in st.session_state:
            line.start_x, line.start_y, line.end_x, line.end_y = st.session_state[key]

    conversion_factor = convert_px_to_m(lines)

    # Redraw the lines on the image
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    for line_key, line in lines.items():
        pixel_length = line.calculate_length()
        meter_length = pixel_length * conversion_factor
        line.annotate_length(draw, meter_length)

    trapezoid.draw(draw)
    

    #==================== CANVAS TEXT ====================#

    # calc & draw half wingspan
    half_wingspan_meters = abs(trapezoid.x_tip - trapezoid.x_root) * conversion_factor
    half_wingspan_line = Line([trapezoid.x_root, trapezoid.y_root + 180, trapezoid.x_tip, trapezoid.y_root + 180], line_color="red", line_width=1)
    half_wingspan_line.draw(draw)
    midpoint = half_wingspan_line.midpoint()
    offset = (20, -20)
    draw_text(draw, f"{half_wingspan_meters:.2f} m", (midpoint[0] + offset[0], midpoint[1] + offset[1]), text_color="red", font_size=20)

    # Update the trapezoid area calculation
    trapezoid_area = 0.5 * half_wingspan_meters * (trapezoid.l_0_px + trapezoid.l_1_px)* conversion_factor
    area_text_position = (pixel_canvas_width - 400, pixel_canvas_height - 250)
    # adjust subscript
    s_text_position = (area_text_position[0] + 22, area_text_position[1] + 28)
    subscript_position = (s_text_position[0], s_text_position[1])
    draw_text(draw, "20", subscript_position, text_color="red", font_size=16)
    draw_text(draw, f"S = {trapezoid_area:.2f} m²", area_text_position, text_color="red", font_size=36)
    
    # canvas legend
    canvas_info_position = (pixel_canvas_width - int(0.32 * pixel_canvas_width), pixel_canvas_height - int(0.12 * pixel_canvas_height))
    draw_text(draw, f"Pixel canvas = {pixel_canvas_width}x{pixel_canvas_height}px", canvas_info_position)
    draw_text(draw, f"1m  = {1/conversion_factor:.4f} px", (canvas_info_position[0], canvas_info_position[1] + 30))
    draw_text(draw, f"1px = {conversion_factor:.4f} m", (canvas_info_position[0], canvas_info_position[1] + 60))

    # render drawing
    draw_all_lines(draw, lines)
    st.image(img)
    
    
    l0 = Variable("Tip Chord Length", trapezoid.l_0_px * conversion_factor, "l_{0}", "m")
    l1 = Variable("Root Chord Length", trapezoid.l_1_px * conversion_factor, "l_{1}", "m")
    b = Variable("Wingspan", half_wingspan_meters*2, "b", "m")  # Use a Variable instance for the wingspan
    
    st.latex(f"S_{{20}} = \\frac{{{l0.latex} + {l1.latex}}}{2} \\cdot \\frac{{{b.latex}}}{2} = \\frac{{{l0.value:.3f} + {l1.value:.3f}}}{2} \\cdot \\frac{{{b.value:.3f}}}{2} = {trapezoid_area:.3f} \\, \\text{{m}}^2")
    st.latex(f"S = S_{{20}} \\cdot 2 = {trapezoid_area*2:.3f} \\, \\text{{m}}^2")

    l0_draw = l0.value
    l1_draw = l1.value
    b_draw = b.value
    S_draw = trapezoid_area * 2

    st.code(half_wingspan_meters)

    with st.expander("Pixel to m conversion accuracy"):
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
        st.markdown(table_markdown)

    bounding_box = trapezoid.get_bounding_box()
    cropped_img = img.crop(bounding_box)
    cropped_img_path = f"./pages/crop{conversion_factor:.6f}.png"
    cropped_img.save(cropped_img_path)
    st.code(f"BOXXXX: {bounding_box}") 
    st.code(f"conversion: {conversion_factor}")
       
    return S_draw, l0_draw, l1_draw, b_draw


if __name__ == "__main__":
    main()