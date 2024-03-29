# ./modules/draw/draw.py
from PIL import Image, ImageDraw, ImageFont, ImageOps
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/base_image_vertical.png"
svg_lines = "./modules/draw/lines.svg"
font_path = './assets/Roboto_Mono/static/RobotoMono-Regular.ttf'

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

def draw_extreme_measurement_lines(draw, lines, font, conversion_factor, offset=200):
    # Find the extreme points by creating lists of all x and y coordinates
    x_coords = [line['start'][0] for line in lines] + [line['end'][0] for line in lines]
    y_coords = [line['start'][1] for line in lines] + [line['end'][1] for line in lines]

    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)

    # Horizontal lines at min_y and max_y
    draw.line([(min_x - offset, min_y), (max_x + offset, min_y)], fill='yellow', width=2)
    draw.line([(min_x - offset, max_y), (max_x + offset, max_y)], fill='yellow', width=2)
    
    # Vertical lines at min_x and max_x
    draw.line([(min_x, min_y - offset), (min_x, max_y + offset)], fill='yellow', width=2)
    draw.line([(max_x, min_y - offset), (max_x, max_y + offset)], fill='yellow', width=2)
    
    # Annotate lines with lengths
    horizontal_length_m = (max_x - min_x) * conversion_factor
    vertical_length_m = (max_y - min_y) * conversion_factor
    
    # Text positioning adjusted to not overlap with lines
    draw.text((max_x + offset*3, (min_y + max_y) / 2), f"{vertical_length_m:.5f}m", fill='red', font=font)
    draw.text(((min_x + max_x) / 2, max_y + offset*3), f"{horizontal_length_m:.5f}m", fill='red', font=font)


def draw_centered_measurement_lines(draw, shape_center, font, conversion_factor):
    # Define lengths for measurement lines (arbitrary lengths or based on shape size)
    line_length = 100  # Adjust based on your preference or dynamic calculations
    # Draw horizontal measurement line centered on centroid
    draw.line([(shape_center[0] - line_length / 2, shape_center[1]), (shape_center[0] + line_length / 2, shape_center[1])], fill='blue', width=2)
    # Draw vertical measurement line centered on centroid
    draw.line([(shape_center[0], shape_center[1] - line_length / 2), (shape_center[0], shape_center[1] + line_length / 2)], fill='blue', width=2)
    # Compute lengths in meters using the conversion factor
    measurement_length_m = line_length * conversion_factor
    # Annotate horizontal line
    draw.text((shape_center[0] + line_length / 2 + 10, shape_center[1]), f"{measurement_length_m:.2f}m", fill='red', font=font)
    # Annotate vertical line
    draw.text((shape_center[0], shape_center[1] - line_length / 2 - 30), f"{measurement_length_m:.2f}m", fill='red', font=font)


# 🔥 ========================= 🔥 draw shapes 🔥 =========================


def draw_shapes_with_lengths(svg_file_path, show_labels=True):
    # Extract lines with color from SVG paths
    lines = extract_lines_from_svg(svg_file_path)

    overall_min_x = float('inf')
    overall_max_x = float('-inf')
    overall_min_y = float('inf')
    overall_max_y = float('-inf')

    img = Image.open(base_image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=26)
    font_area = ImageFont.truetype(font_path, size=42)

    shapes = []  # List to store shape data
    temp_shape = []  # Temporary list to store lines of a shape

    for line in lines:
        start, end, color = line
        start_pixels = (start[0], start[1])
        end_pixels = (end[0], end[1])

        # Update the overall extremes
        overall_min_x = min(overall_min_x, start_pixels[0], end_pixels[0])
        overall_max_x = max(overall_max_x, start_pixels[0], end_pixels[0])
        overall_min_y = min(overall_min_y, start_pixels[1], end_pixels[1])
        overall_max_y = max(overall_max_y, start_pixels[1], end_pixels[1])

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
            
            # Draw the area annotation
            offset_x, offset_y = 60, -160
            # offset_x, offset_y = 0, -42
            text_position = (shape_center[0] + offset_x, shape_center[1] + offset_y)
            draw.text(text_position, f"{area:.3f} m²", fill=color, font=font_area)
            
            # draw_extreme_measurement_lines(draw, temp_shape, font, conversion_factor, offset=20)

            # draw_centered_measurement_lines(draw, shape_center, font, conversion_factor)
            
            shape = Shape(temp_shape)
            shape.area = area
            shapes.append(shape)
            temp_shape = []

    draw_extreme_measurement_lines(draw, [
        {'start': (overall_min_x, overall_min_y), 'end': (overall_max_x, overall_min_y)},
        {'start': (overall_min_x, overall_max_y), 'end': (overall_max_x, overall_max_y)},
        {'start': (overall_min_x, overall_min_y), 'end': (overall_min_x, overall_max_y)},
        {'start': (overall_max_x, overall_min_y), 'end': (overall_max_x, overall_max_y)}
    ], font, conversion_factor, offset=20)

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
