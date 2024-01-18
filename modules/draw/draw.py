# ./modules/draw/draw.py
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/drawing.png"
svg_lines = "./modules/draw/lines.svg"
font_path = './assets/Roboto_Mono/static/RobotoMono-Regular.ttf'


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

#========================= shapes =========================
def extract_lines_from_svg(svg_file_path):
    paths, attributes = svg2paths(svg_file_path)
    lines = []

    for path in paths:
        for line in path:
            start = (line.start.real, line.start.imag)
            end = (line.end.real, line.end.imag)
            lines.append((start, end))

    return lines

def draw_lines_and_display_lengths(svg_file_path):

    # Extract lines from SVG paths
    lines = extract_lines_from_svg(svg_file_path)

    img = Image.open(base_image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=22)
    lengths = []  # List to store lengths of all lines

    for line in lines:
        start, end = line
        start_pixels = (start[0], start[1])
        end_pixels = (end[0], end[1])

        # Draw the line on the image
        draw.line([start_pixels, end_pixels], fill='red', width=3)

        # Calculate the length of the line in meters
        length_pixels = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
        length_meters = length_pixels * conversion_factor
        lengths.append(length_meters) # Append length to the list

        # Find the midpoint for the text label using the SVG coordinates
        midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        length_text = f"{length_meters:.2f}m"

        # Display the length of the line on the image using the SVG's coordinate system
        draw.text(midpoint, length_text, fill='blue', font=font)

    return img, lengths

# if __name__ == "__main__":
#     base_image = "./modules/draw/drawing.png"
#     svg_lines = "./modules/draw/lines.svg"
#     _, conversion_factor = parse_svg_for_lines(svg_lines)
#     lines = extract_lines_from_svg(svg_lines)
#     img = draw_lines_and_display_lengths(base_image, lines, conversion_factor, './assets/Roboto_Mono/static/RobotoMono-Regular.ttf')
#     st.image(img)  # Or save the image if you prefer
