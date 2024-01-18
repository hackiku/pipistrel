### ./pages/s20.py
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import svg2paths, parse_path
from modules.draw.draw import draw_measurements_on_image, parse_svg_for_lines

def extract_shapes_from_svg(svg_file_path):
    paths, attributes = svg2paths(svg_file_path)
    shapes = {'trapezoids': []}

    # We are now treating all paths as potential trapezoids.
    for path, attribute in zip(paths, attributes):
        # Extract the points for the shape from the path
        shape_points = [(seg.start.real, seg.start.imag) for seg in path]
        # Ensure we add the last point of the path if it's not already included
        if shape_points[0] != (path[-1].end.real, path[-1].end.imag):
            shape_points.append((path[-1].end.real, path[-1].end.imag))
        shapes['trapezoids'].append(shape_points)

    return shapes


def draw_shapes_and_calculate_areas(image_path, shapes, conversion_factor):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('./assets/Roboto_Mono/static/RobotoMono-Regular.ttf', size=22)
    area_data = {}

    for i, shape_points in enumerate(shapes['trapezoids']):
        # Use the SVG coordinates directly for the polygon points
        points_pixels = [(p[0], p[1]) for p in shape_points]

        # Calculate the area in pixels, then convert to square meters
        area_pixels = calculate_polygon_area(points_pixels)
        area_meters = area_pixels * conversion_factor**2

        # Draw the shape on the image
        draw.polygon(points_pixels, outline='purple', width=3)

        # Calculate the centroid for the text label
        centroid = tuple(map(sum, zip(*points_pixels)))  # Simple centroid calculation
        centroid = (centroid[0] / len(points_pixels), centroid[1] / len(points_pixels))
        
        # Flip the y-coordinate of the centroid for text placement
        text_centroid = (centroid[0], img.size[1] - centroid[1])
        
        area_text = f"{area_meters:.2f} m²"
        draw.text(text_centroid, area_text, fill='red', font=font)

        # Store the area data
        area_data[f"trapezoid_{i}"] = area_meters

    return img, area_data


def calculate_polygon_area(vertices):
    # Initialize area
    area = 0.0
    # Calculate the area using the shoelace formula
    for i in range(len(vertices)):
        j = (i + 1) % len(vertices)  # Next vertex index
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    area = abs(area) / 2.0
    return area


def main():
    st.subheader("Wing area calculations")

    base_image = "./modules/draw/drawing.png"
    svg_file_path = './modules/draw/s20.svg'
    
    # st.image(svg_file_path)
    # Get conversion factor from draw.py
    _, conversion_factor = parse_svg_for_lines(svg_file_path)

    if conversion_factor == 0:
        st.error("Conversion factor is zero, check your SVG lines and units.")
        st.stop()

    # Extract shapes from SVG
    shapes = extract_shapes_from_svg(svg_file_path)

    # Draw shapes and calculate areas
    img, area_data = draw_shapes_and_calculate_areas(base_image, shapes, conversion_factor)
    
    # Display the image with drawn shapes
    st.image(img, caption='Wing with calculated areas')

    # Display area calculations
    for area_description, area_value in area_data.items():
        st.write(f"{area_description}: {area_value:.2f} m²")
    
    st.code(f"Conversion factor: {conversion_factor:.6f}")

if __name__ == "__main__":
    main()
