# ./pages/5_Fuselage_drag.py

import streamlit as st
from PIL import Image, ImageOps
from utils import spacer, final_value_input_oneline
from modules.draw.draw import draw_shapes_with_lengths, crop_image, calculate_area
from variables_manager import initialize_session_state, get_variable_value,\
    get_variable_props, display_variable, update_variables, log_changed_variables

# Define a dictionary for each projection with its details
projections_details = {
    'side': {'name': 'Side Projection (1/3)', 'svg_path': './modules/draw/fuselage_draw/fuselage_side.svg', 'crop_y': (0, 650)},
    'planform': {'name': 'Planform Projection (2/3)', 'svg_path': './modules/draw/fuselage_draw/fuselage_planform.svg', 'crop_y': (1500, 3000)},
    'front': {'name': 'Front Projection (1/3)', 'svg_path': './modules/draw/fuselage_draw/fuselage_front.svg', 'crop_y': (650, 1500)},
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

# =================================================================== #
# ======================= MAIN ====================================== #
# =================================================================== #

def main():
    st.title("Fuselage areas Calculation")

    page_values = [
        'S', 'v_krst', 'nu'
    ]

    initialize_session_state()

    
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
            st.latex(f"S_{{Tpl}} = \\sum_{{i=1}}^{len(shapes)} S_i = {S_tpl:.3f} \\, \\text{{m}}^2")
            st.markdown("***")
        elif key == 'side':
            S_tb = total_area
            st.markdown(f"**Total Side Projection Area `S_tb`:**")
            st.latex(f"S_{{Tb}} = \\sum_{{i=1}}^{len(shapes)} S_i = {S_tb:.3f} \\, \\text{{m}}^2")
            st.markdown("***")
        elif key == 'front':
            S_max = total_area
            st.markdown(f"**Maximum Cross-Sectional Area `S_max`:**")
            st.latex(f"S_{{max}} = \\sum_{{i=1}}^{len(shapes)} S_i = {S_max:.3f} \\, \\text{{m}}^2")
            st.markdown("***")


    st.markdown("***")
    st.markdown("***")




    # ====================================================================================
    # ====================================================================================
    st.markdown("***") # =================================================================
    st.markdown("***") # =================================================================
    # ====================================================================================
    # ====================================================================================


    # ===================== areas =====================

    col1, col2 = st.columns(2)
    with col1:
        S_tb_input = st.number_input("Total side projection area `S_tb` (m²)", value=S_tb, format="%.3f")
        S_tb = S_tb_input
        st.latex(f"S_{{Tb}} = {S_tb:.3f}  \\, \\text{{m}}^2")
    with col2:
        S_tpl_input = st.number_input("Total planform area `S_tpl` (m²)", value=S_tpl, format="%.3f")
        S_tpl = S_tpl_input
        st.latex(f"S_{{Tpl}} = {S_tpl:.3f}  \\, \\text{{m}}^2")

    S_wet = (S_tpl + S_tb) * (2 - 0.4 * (S_tpl / S_tb))
    st.latex(f"S_{{wet}} = (S_{{Tpl}} + S_{{Tb}}) \\cdot (2 - 0.4 \\cdot \\frac{{S_{{Tpl}}}}{{S_{{Tb}}}})")
    st.latex(f"S_{{wet}} = ({S_tpl:.3f} + {S_tb:.3f}) \\cdot (2 - 0.4 \\cdot \\frac {{{S_tpl:.3f}}} {{{S_tb:.3f}}}) = {S_wet:.3f} \, m^2")

    spacer()
    
    st.write("The frontal projection area represents the maximum cross-sectional area `S_max`")
    
    S_max_input = st.number_input("Change max cross-sectional area `S_max` (m²)", value=S_max, format="%.3f")    
    S_max = S_max_input
    st.latex(f"S_{{max}} = {S_max:.3f}  \\, \\text{{m}}^2")
    
    st.markdown("***")
    
    # ===================== equivalent diameter =====================

    st.write("The equivalent diameter `D` is derived from imagining the maximum cross-sectional area as a circle. It's instrumental in calculating the fuselage's fineness ratio.")

    D = (4 * S_max / 3.14159) ** 0.5
    st.latex(f"D = \\sqrt{{\\frac{{4 \\cdot {S_max:.3f}}}{{\\pi}}}} = {D:.3f} \\, m")


    # ===================== fineness ratio =====================
    col1, col2 = st.columns(2)
    with col1:
        D_input = st.number_input("Change equivalent diameter `D` (m)", value=D, format="%.3f")
        D = D_input
        st.latex(f"D = {D:.3f}  \\, \\text{{m}}")
    with col2:
        L = st.number_input("Fuselage length `L` (m)", value=10.37, format="%.3f")
        st.latex(f"L = {L}  \\, \\text{{m}}")
    
    fineness_ratio = L / D
    
    st.latex(f"\\frac{{L}}{{D}} = \\frac{{{L:.2f}}}{{{D:.3f}}} = {fineness_ratio:.2f}")
    
    st.markdown("***")
    
    # ======================== form factor K ======================= #

    col1, col2 = st.columns(2)
    with col1:
        fineness_ratio_input = st.number_input("Change fineness ratio (L/D)", value=fineness_ratio, format="%.2f")
    with col2:
        st.latex(f"\\frac{{L}}{{D}} = {fineness_ratio:.3f}")
    
    spacer()
    
    st.image('./assets/tmp_assets/koef_min_otpora.png', )
    
    spacer()
    
    col1, col2 = st.columns(2)
    with col1:
        K = st.number_input("Form factor K", value=1.2, format="%.2f")
        st.latex(f"K = {K}")
    with col2:
        delta_K = st.number_input("Roughness correction factor", value=1.1, format="%.1f", step=0.1)
        st.latex(f"\\Delta K = {delta_K:.1f}")
    
    # =================== Reynolds number =================== #
    
    st.subheader("Reynolds number for fuselage")
    col1, col2 = st.columns(2)
    with col1:
        v_krst_input = st.number_input("v_krst (m/s)", get_variable_value("v_krst"), format="%.3f")
        v_krst = v_krst_input
    with col2:
        nu_input = st.number_input("nu (m²/s)", get_variable_value("nu"), format="%.3e")
        nu = nu_input
    
    Re = v_krst * L / nu
    
    st.latex(rf"Re = \frac{{v_{{krst}} \cdot L }}{{\nu}} = \frac{{{v_krst:.2f} \cdot {L:.3f}}}{{{nu:.2e}}} \approx {Re:.3e}")

    spacer()
    
    st.markdown("""
    <div style="background-color: black; opacity: 0.3; padding: 100px"></div>""", unsafe_allow_html=True)

    spacer()
    
    col1, col2 = st.columns(2)
    with col1:
        Cf = st.number_input("Read skin friction coefficient `C_f` from graph based on Re", value=0.003, format="%.5f")
    with col2:
        st.latex(f"C_{{f}} = {Cf:4f}")

    st.markdown("***")



    # ====================================================================
    # ===================== Minimal Drag Fuselage ========================
    # ====================================================================

    st.write("Calculating the minimum drag coefficient ($ C_{X_{min}} $) for the fuselage, incorporating the effects of shape through the K factor and skin friction through `C_f`:")

    S = get_variable_value("S")
    Cx_min_fus = K * Cf * S_wet / S
    st.write(Cx_min_fus)
    # st.latex(r"C_{X min ht} = \frac{K_{HR_{ht}} \cdot C_{fHT} \cdot S_{WETHT}}{S} = \frac{1.135 \cdot 0.00305 \cdot 16.153}{20.602} = 0.002714")

    st.latex(rf"(C_{{X \, \text{{min}}}})_{{\text{{trup}}}} = \frac{{K_{{\text{{trup}}}} \cdot C_{{f_{{\text{{trup}}}}}} \cdot S_{{WET_{{\text{{trup}}}}}}}}{{S}} = \frac{{{K:.3f} \cdot {Cf:.5f} \cdot {S_wet:.3f}}}{{{S:.3f}}} = {Cx_min_fus:.6f}")
    
    spacer()

    st.markdown("***")

    success_message = "$$ C_{{X_{{min}}}} = {:.5f}^{{\\circ}} $$"
    warning_message = "$$ C_{{X_{{min}}}} = {:.5f}^{{\\circ}} $$"

    Cx_min_fus = final_value_input_oneline(
        "Fuselage min drag coefficient",
        Cx_min_fus,
        success_message,
        warning_message
    )
    st.write(Cx_min_fus)

    st.markdown("***")
    st.markdown("***")
    
    
    # ========================= debug markdown tables =========================
    with st.expander("Fuselage Area Calculations"):
        markdown_content = ""
        markdown_content += "| Area | Value (m²) |\n"
        markdown_content += "| ---- | ----------- |\n"
        markdown_content += f"| S_tpl | {S_tpl:.3f} |\n"
        markdown_content += f"| S_tb | {S_tb:.3f} |\n"
        markdown_content += f"| S_max | {S_max:.3f} |\n"
        # markdown_content += f"| S_exp | {S_exp:.3f} |\n"
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
