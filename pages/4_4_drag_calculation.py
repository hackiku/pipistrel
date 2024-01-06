# 4_drag_calculation.py

import streamlit as st
import matplotlib.pyplot as plt


def main():

    def simple_plot():
        x = list(range(1, 11))  # Numbers 1 through 10
        y = x  # Same as x, so we get a straight line

        plt.plot(x, y)
        st.pyplot()
    
    simple_plot()

if __name__ == "__main__":
    main()



    #==================== PLOT ====================#
    
    def find_image_with_conversion_factor(directory, pattern):
        # Compile the regex pattern
        regex = re.compile(pattern)
        for filename in os.listdir(directory):
            if regex.match(filename):
                # Extract the conversion factor from the filename
                conversion_factor = float(regex.findall(filename)[0])
                return os.path.join(directory, filename), conversion_factor
        return None, None

    def draw_flow_separation():
        # Find background image and conversion factor
        pattern = r"crop(\d+\.\d+).png"
        directory = './pages'
        img_path, conversion_factor = find_image_with_conversion_factor(directory, pattern)
        st.code(f'conversion factor: {conversion_factor}')

        # If the image is found and the conversion factor is extracted
        if img_path and conversion_factor:
            img = mpimg.imread(img_path)
            
            img_aspect_ratio = img.shape[0] / img.shape[1]
            fig_width = 12 # You can adjust this width as needed
            fig, ax = plt.subplots(figsize=(fig_width, fig_width * img_aspect_ratio))
            
            cz_max = max(2, img.shape[0] * conversion_factor)
            background_size = [0, 1, 0, cz_max]
            
            # Display the background image
            ax.imshow(img, extent=background_size, aspect='auto')

        ax.plot(y_b2.value, c_z_max.value, label='Czmax - ap', marker='o', linestyle='-')
        ax.plot(c_z_max_cb_ca.value, label='Czmax - Cb/Ca', marker='o', linestyle='-')
        ax.plot(c_z_lok.value, label='Czlok - Airfoil', marker='o', linestyle='-')


        # Set labels and title
        ax.set_xlabel('y/(b/2)')
        ax.set_ylabel('Cz')
        ax.set_title('Cz distribution along wing span')

        # plot
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    draw_flow_separation()
