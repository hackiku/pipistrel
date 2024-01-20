# ./pages/draw_fuselage_areas.py
import streamlit as st
from PIL import Image, ImageOps
from modules.draw.draw import draw_shapes_with_lengths, crop_image

# Define a dictionary for each projection with its details
projections_details = {
    'side': {'name': 'Side Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_side.svg', 'crop_y': (0, 650)},
    'front': {'name': 'Front Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_front.svg', 'crop_y': (650, 1500)},
    'planform': {'name': 'Planform Projection', 'svg_path': './modules/draw/fuselage_draw/fuselage_planform.svg', 'crop_y': (1500, 3000)},
}

def draw_fuselage_area(projection_details, key, show_labels=True):

    # choose color inversion and measurements
    col1, col2 = st.columns(2)
    with col1:
        invert_choice = st.radio("Color", ["Black", "White"], index=0, key=f"invert_choice_{key}")
    with col2:
        labels_choice = st.radio("Show measures", ["All", "Area only"], index=0, key=f"labels_choice_{key}")
        show_labels = labels_choice != "Area only"

    # draw the shapes    
    img, shapes, lines = draw_shapes_with_lengths(projection_details['svg_path'], show_labels)
    
    # invert image colors (defailt to )
    if invert_choice == "Black":
        img = ImageOps.invert(img.convert('RGB'))

    cropped_img = crop_image(img, *projection_details['crop_y'])
    st.image(cropped_img, caption=projection_details['name'])

    return shapes, lines

def main():
    st.title("Fuselage Area Calculation")
    
    # Initialize dictionaries to store individual areas and LaTeX strings
    individual_areas = {'side': {}, 'front': {}, 'planform': {}}
    latex_sum_strs = {'side': "", 'front': "", 'planform': ""}

    # Initialize variables for total areas
    S_tpl, S_tb, S_max = 0, 0, 0

    # Process each projection
    for key, details in projections_details.items():
        
        st.markdown(f"### {details['name']}")
        shapes, lines = draw_fuselage_area(details, key)
        latex_sum_with_indices = " + ".join([f"S_{{{i+1}}}" for i in range(len(shapes))])

        # Initialize markdown table rows for names and values
        markdown_area_names = "| Area "
        markdown_area_values = "| Value (m²) "
        latex_areas_sum_names = ""
        latex_areas_sum_values = ""

        # Display the title for each projection

        for i, shape in enumerate(shapes):
            area = shape.area
            individual_areas[key][f'S{i+1}'] = area

            # Append to markdown rows using dollar signs for LaTeX in markdown
            markdown_area_names += f"| $S_{{{i+1}}}$ "
            markdown_area_values += f"| {area:.3f} "

            # Append to LaTeX sum strings
            latex_areas_sum_names += f"S_{{{i+1}}} + "
            latex_areas_sum_values += f"{area:.3f} + "

        markdown_area_names += "|"
        markdown_area_values += "|"

        # Remove the last ' + ' from the LaTeX sum strings
        latex_areas_sum_names = latex_areas_sum_names.rstrip(' + ')
        latex_areas_sum_values = latex_areas_sum_values.rstrip(' + ')

        # Calculate total area for the current projection
        total_area = sum(individual_areas[key].values())

        # Display the markdown table with two rows
        markdown_table_divider = "| --- " * (len(shapes) + 1) + "|"
        # markdown_table_divider = "|" + " --- |" * 2
        markdown_table = markdown_area_names + "\n" + markdown_table_divider + "\n" + markdown_area_values
        st.markdown(markdown_table)

        # Display the LaTeX sums
        st.latex(f"S_{{total}} = {latex_areas_sum_names} = {total_area:.3f} \\, \\text{{m}}^2")
        st.latex(f"S_{{total}} = {latex_areas_sum_values} = {total_area:.3f} \\, \\text{{m}}^2")

        # Store the LaTeX string for sums
        latex_sum_strs[key] = latex_areas_sum_names

        # Assign the total area to the corresponding variable and display
        if key == 'planform':
            S_tpl = total_area
            st.markdown(f"**Total Planform Area `S_tpl`:** {S_tpl:.3f} m²")
            st.latex(f"S_{{tpl}} = \\sum_{{i=1}}^{len(shapes)} S_i = {latex_sum_with_indices} = {S_tpl:.3f} \\, \\text{{m}}^2")
            st.markdown("***")
        elif key == 'side':
            S_tb = total_area
            st.markdown(f"**Total Side Projection Area `S_tb`:**")
            st.latex(f"S_{{tb}} = \\sum_{{i=1}}^{len(shapes)} S_i = {latex_sum_with_indices} = {S_tb:.3f} \\, \\text{{m}}^2")
            st.markdown("***")
        elif key == 'front':
            S_max = total_area
            st.markdown(f"**Maximum Cross-Sectional Area `S_max`:**")
            st.latex(f"S_{{max}} = \\sum_{{i=1}}^{len(shapes)} S_i = {latex_sum_with_indices} = {S_max:.3f} \\, \\text{{m}}^2")
            st.markdown("***")


    st.markdown("##### Fuselage Area from Drawing")
    st.markdown("#### Area Calculations")
    
    st.markdown(f"**Total Planform Area (S_tpl):** {S_tpl:.3f} m²")
    st.latex(f"S_{{tpl}} = {S_tpl:.3f}  \\, \\text{{m}}^2")
    
    st.markdown(f"**Total Side Projection Area (S_tb):** {S_tb:.3f} m²")
    st.latex(f"S_{{tb}} = {S_tb:.3f}  \\, \\text{{m}}^2")
    
    st.markdown(f"**Maximum Cross-Sectional Area (S_max):** {S_max:.3f} m²")
    st.latex(f"S_{{max}} = {S_max:.3f}  \\, \\text{{m}}^2")

    S_exp = shapes[0].area  # Assuming shapes[0] is the fuselage exposed area
    st.latex(f"S_{{exp}} = {S_exp:.3f}  \\, \\text{{m}}^2")

    l0 = shapes[0].lines[1]['length_meters']  # Base length of the fuselage
    lt = shapes[0].lines[3]['length_meters']  # Top length of the fuselage

    # Calculate wetted area (S_wet)
    S_wet = (S_tpl + S_tb) - (2 - 0.4 * (S_tpl / S_tb)) * (S_tpl / S_tb)
    st.markdown(f"**Wetted Area (S_wet):** {S_wet:.3f} m²")

    # Calculate equivalent diameter (D)
    D = ((4 * S_max) / 3.14159)**0.5
    st.markdown(f"**Equivalent Diameter (D):** {D:.3f} m")

    # Given fuselage length (L)
    L = 12.942  # This value appears to be given in the document
    st.markdown(f"**Fuselage Length (L):** {L:.3f} m")
    
    with st.expander("Fuselage Area Calculations"):
        markdown_content = ""
        markdown_content += "| Area | Value (m²) |\n"
        markdown_content += "| ---- | ----------- |\n"
        markdown_content += f"| S_tpl | {S_tpl:.3f} |\n"
        markdown_content += f"| S_tb | {S_tb:.3f} |\n"
        markdown_content += f"| S_max | {S_max:.3f} |\n"
        markdown_content += f"| S_exp | {S_exp:.3f} |\n"
        markdown_content += f"| S_wet | {S_wet:.3f} |\n"
        markdown_content += f"| D | {D:.3f} |\n"
        markdown_content += f"| L | {L:.3f} |\n"
        st.markdown(markdown_content)
        st.write(lines)

    with st.expander("Line Lengths"):
        markdown_content = ""
        for i, shape in enumerate(shapes):
            markdown_content += f"### Shape {i+1}\n"
            markdown_content += "| Line | Length (m) |\n"
            markdown_content += "| ---- | ---------- |\n"
            for j, line_dict in enumerate(shape.lines):
                markdown_content += f"| Line {j+1} | {line_dict['length_meters']:.3f} |\n"    

        st.markdown(markdown_content)


if __name__ == "__main__":
    main()
