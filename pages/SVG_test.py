import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import svg2paths

# Path to the base image and SVG file
base_image = "./modules/draw/base_image.png"
svg_lines = "./modules/draw/lines.svg"

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
            st.code(line_info)  # Log the parsed line information 
            # st.code(f"Line from {start} to {end}: {pixel_length}px computed, {real_size_m:.3f}m real")

            total_pixels += length_pixels
            total_meters += real_size_m

    conversion_factor = total_meters / total_pixels if total_pixels else 0
    st.write(f"Total real length (meters): {total_meters}")
    st.write(f"Total length (pixels): {total_pixels}")
    st.write(f"Conversion factor: {conversion_factor:.6f} m/px")
    
    return lines, conversion_factor

def draw_measurements_on_image(image_path, lines, conversion_factor):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=22)

        for line in lines:
            start, end = line['start'], line['end']
            real_length_m = line['real_length_m']
            computed_length_m = line['length_pixels'] * conversion_factor
            error_percentage = ((computed_length_m - real_length_m) / real_length_m) * 100
            st.write(f"Line Real Length: {real_length_m}m, Computed Length: {computed_length_m}m, Error: {error_percentage}%")
            draw.line([start, end], fill='blue', width=3)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            text = f"{real_length_m:.2f}m ({line['length_pixels']:.2f}px, {error_percentage:.1f}%)"
            draw.text(midpoint, text, fill='red', font=font)
        st.image(img)

def main():
    st.title("SVG Line Measurements")
    lines, conversion_factor = parse_svg_for_lines(svg_lines)
    draw_measurements_on_image(base_image, lines, conversion_factor)

if __name__ == "__main__":
    main()