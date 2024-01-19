# ./modules/draw/draw.py
from PIL import Image, ImageDraw, ImageFont, ImageOps
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/base_image.png"
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

# ========================= draw shapes  =========================
def draw_shapes_with_lengths(svg_file_path):
    # Extract lines with color from SVG paths
    lines = extract_lines_from_svg(svg_file_path)

    img = Image.open(base_image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=22)
    font_area = ImageFont.truetype(font_path, size=32)

    shapes = []  # List to store shape data
    temp_shape = []  # Temporary list to store lines of a shape

    for line in lines:
        start, end, color = line
        start_pixels = (start[0], start[1])
        end_pixels = (end[0], end[1])

        # Draw the line on the image
        draw.line([start_pixels, end_pixels], fill=color, width=3)

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
        midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        draw.text(midpoint, f"{length_meters:.2f}m", fill='blue', font=font)

        # If temp_shape has 4 lines, calculate area and create a Shape
        if len(temp_shape) == 4:
            area = calculate_area(temp_shape)
            shape_center = calculate_shape_center(temp_shape)
            
            offset_x, offset_y = -60, 30
            text_position = (shape_center[0] + offset_x, shape_center[1] + offset_y)
            
            draw.text(text_position, f"{area:.3f} m²", fill=color, font=font_area)
            
            shape = Shape(temp_shape)
            shape.area = area
            shapes.append(shape)
            temp_shape = []

    return img, shapes, lines

### TODO redrawing shapes blah
def redraw_shapes(img, shapes):
    
    img, shapes, lines = draw_shapes_with_lengths(svg_file_path)

    draw = ImageDraw.Draw(original_image)
    font = ImageFont.truetype(font_path, size=22)

    for shape in shapes:
        for line in shape:
            start, end, length, color = line
            # Logic to adjust the end point based on the new length
            # and redraw the line
            # ...

    return original_image

def crop_image(img, crop_height, invert=False):

    width, height = img.size
    cropped_img = img.crop((0, height - crop_height, width, height))

    if invert:
        cropped_img = ImageOps.invert(cropped_img.convert('RGB'))

    return cropped_img