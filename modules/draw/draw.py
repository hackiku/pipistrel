# ./modules/draw/draw.py
from PIL import Image, ImageDraw, ImageFont, ImageOps
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/base_image_vertical.png"
svg_lines = "./modules/draw/lines.svg"
font_path = './assets/Roboto_Mono/static/RobotoMono-Regular.ttf'
font_bold = './assets/Roboto_Mono/static/RobotoMono-Bold.ttf'

class Shape:
    def __init__(self, lines):
        self.lines = lines  # Directly assign the list of dictionaries to self.lines
        self.color = lines[0]['color']  # Access color using dictionary key
        self.area = 0  # Initialize area, to be calculated later


# measurement lines parsing
def parse_svg_for_lines(svg_file):
    paths, attributes = svg2paths(svg_file)
    lines = []
    real_sizes_mm = [6495, 10710, 1490, 1095, 1610, 1000, 2175, 3210, 4855, 1100, 920, 1100, 1130, 738, 1640, 630, 1170, 1820, 570, 340]
    real_sizes_m = [size_mm / 1000 for size_mm in real_sizes_mm]
    total_pixels = total_meters = 0

    for path, real_size_m in zip(paths, real_sizes_m):
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            length_pixels = abs(line.length())
            line_info = {
                'start': start, 
                'end': end, 
                'length_pixels': length_pixels, 
                'real_length_m': real_size_m,
                'computed_length_m': length_pixels / 1000  # Assuming 1 pixel = 1 mm for initial calculation
            }
            line_info = {'start': start, 'end': end, 'length_pixels': length_pixels, 'real_length_m': real_size_m}
            lines.append(line_info)
            print(line_info)  # Log the parsed line information 
            # st.code(f"Line from {start} to {end}: {pixel_length}px computed, {real_size_m:.3f}m real")

            total_pixels += length_pixels
            total_meters += real_size_m
            
    conversion_factor = total_meters / total_pixels if total_pixels else 0
    
    return lines, conversion_factor

# measurement lines drawing
def draw_measurements_on_image(lines, conversion_factor):
    with Image.open(base_image) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, size=22)

        for line in lines:
            start, end = line['start'], line['end']
            real_length_m = line['real_length_m']
            computed_length_m = line['length_pixels'] * conversion_factor
            error_percentage = ((computed_length_m - real_length_m) / real_length_m) * 100
            print(f"Line Real Length: {real_length_m}m, Computed Length: {computed_length_m}m, Error: {error_percentage}%")
            draw.line([start, end], fill='blue', width=3)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m ({line['length_pixels']:.2f}px, {error_percentage:.1f}%)"
            draw.text(midpoint, text, fill='red', font=font)
        return img

lines, conversion_factor = parse_svg_for_lines(svg_lines)

draw_measurements_on_image(lines, conversion_factor)



#==========================================================
#========================= shapes =========================
#==========================================================

def extract_lines_from_svg(svg_file_path):
    paths, attributes = svg2paths(svg_file_path)
    lines_with_color = []

    for path, attr in zip(paths, attributes):
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            color = attr.get('stroke', '#FF0000')  # Default to black if no stroke color
            lines_with_color.append((start, end, color))

    return lines_with_color

def calculate_area(lines):
    # Extracting lengths from line dictionaries
    a = lines[0]['length_meters']  # 1st line
    b = lines[2]['length_meters']  # 3rd line
    # height: 2nd and 4th lines
    h = max(lines[1]['length_meters'], lines[3]['length_meters'])
    return 0.5 * (a + b) * h

def calculate_shape_center(lines):
    # Calculate the average of the x and y coordinates of all line endpoints
    x_coords = [line['start'][0] for line in lines] + [line['end'][0] for line in lines]
    y_coords = [line['start'][1] for line in lines] + [line['end'][1] for line in lines]
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    return (center_x, center_y)


def draw_min_max_measurement_lines(draw, shapes, font, conversion_factor):
    fill = 'black'  # Main text color
    shadow_color = 'white'  # Shadow color for text

    font = ImageFont.truetype(font_path, size=26)
    shadow_font = ImageFont.truetype(font_bold, size=24)

    if not shapes:
        return  # Exit if shapes list is empty

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for shape in shapes:
        for line in shape.lines:
            start, end = line['start'], line['end']
            min_x = min(min_x, start[0], end[0])
            max_x = max(max_x, start[0], end[0])
            min_y = min(min_y, start[1], end[1])
            max_y = max(max_y, start[1], end[1])

    # Draw the extreme measurement lines
    horizontal_line_y = max_y + 50
    vertical_line_x = max_x + 80

    draw.line([(min_x, horizontal_line_y), (max_x, horizontal_line_y)], fill=fill, width=3)
    draw.line([(vertical_line_x, min_y), (vertical_line_x, max_y)], fill=fill, width=3)

    # Calculate midpoints for text annotations
    horizontal_text_x = min_x + (max_x - min_x) / 2
    vertical_text_y = min_y + (max_y - min_y) / 2

    # Total length and width calculated for annotation
    total_width_m = (max_x - min_x) * conversion_factor
    total_length_m = (max_y - min_y) * conversion_factor

    # Function to draw text with shadow
    def draw_text_with_shadow(position, text, font, fill, shadow_color):
        shadow_offset = (0, 0)  # Shadow offset; adjust as needed
        # Draw shadow
        draw.text((position[0] + shadow_offset[0], position[1] + shadow_offset[1]), text, font=shadow_font, fill=shadow_color, anchor="mm")
        # Draw main text
        draw.text(position, text, font=font, fill=fill, anchor="mm")

    draw_text_with_shadow((horizontal_text_x, horizontal_line_y + 20), f"{total_width_m:.3f}m", font, fill, shadow_color)
    draw_text_with_shadow((vertical_line_x + 20, vertical_text_y), f"{total_length_m:.3f}m", font, fill, shadow_color)


# 🔥 ========================= 🔥 draw shapes 🔥 =========================
# 🔥 =========================🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥 =========================

def draw_shapes_with_lengths(svg_file_path, show_labels=True):
    # Extract lines with color from SVG paths
    lines = extract_lines_from_svg(svg_file_path)

    img = Image.open(base_image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=26)
    font_area = ImageFont.truetype(font_path, size=42)

    shapes = []  # List to store shape data
    temp_shape = []  # Temporary list to store lines of a shape
    centers = []  # List to store the center of each shape


    for line in lines:
        start, end, color = line
        start_pixels = (start[0], start[1])
        end_pixels = (end[0], end[1])

        # Draw the line on the image
        draw.line([start_pixels, end_pixels], fill=color, width=4)

        # Calculate the length of the line in meters
        length_pixels = ((end[0] - start[0])**2 + (end[1] - start[1])**2)**0.5
        length_meters = length_pixels * conversion_factor

        # Add line as a dictionary to temp_shape
        temp_shape.append({
            'start': start,
            'end': end,
            'length_meters': length_meters,
            'color': color
        })

        # Find the midpoint for the text label using the SVG coordinates
        if show_labels:
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            draw.text(midpoint, f"{length_meters:.3f}m", fill='blue', font=font)

        # If temp_shape has 4 lines, calculate area and create a Shape
        if len(temp_shape) == 4:
            area = calculate_area(temp_shape)
            shape_center = calculate_shape_center(temp_shape)
            centers.append(shape_center)
            
            # Draw individual areas            
            offset_x, offset_y = -50, -180
            # offset_x, offset_y = 0, -42
            text_position = (shape_center[0] + offset_x, shape_center[1] + offset_y)
            draw.text(text_position, f"{area:.3f} m²", fill=color, font=font_area)
                        
            shape = Shape(temp_shape)
            shape.area = area
            shapes.append(shape)
            temp_shape = []

    total_area = sum(shape.area for shape in shapes)
    
    if centers:
        avg_center_x = sum(x for x, y in centers) / len(centers)
        avg_center_y = sum(y for x, y in centers) / len(centers)
        img_size = img.size

        if avg_center_y > img_size[1] * 0.7:
            # Lower part of the image is crowded, place annotation towards the top
            position_y = img_size[1] * 0.90  # 10% from the top
        else:
            # Default to bottom placement with adjustments
            position_y = img_size[1] * 0.9  # 90% from the top

        if avg_center_x > img_size[0] * 0.8:
            # Right half of the image is crowded, place annotation towards the left
            position_x = img_size[0] * 0.1  # 10% from the left
        else:
            # Default to right placement with adjustments
            position_x = img_size[0] * 0.9  # 90% from the left

        def draw_total_area(draw, total_area, position, font_path=font_path):
            font_area_sum = ImageFont.truetype(font_path, size=48)
            text = f"S_tot = {total_area:.3f} m²"
            draw.text(position, text, fill='green', font=font_area_sum)
            # draw.text((position_x+20, position_y+30), f"{avg_center}", fill='red', font=font_area_sum)

        # Call with calculated position
        draw_total_area(draw, total_area, (position_x, position_y))

    draw_min_max_measurement_lines(draw, shapes, font, conversion_factor)

    return img, shapes, lines


def crop_image(img, y_top, y_bottom):
    width, height = img.size
    # Ensure the y-coordinates are within the image bounds
    y_top = max(0, min(y_top, height))
    y_bottom = max(0, min(y_bottom, height))
    
    # Create the crop coordinates (left, upper, right, lower)
    crop_coordinates = (0, y_top, width, y_bottom)

    cropped_img = img.crop(crop_coordinates)

    return cropped_img
