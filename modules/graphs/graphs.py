# ./modules/graphs/graphs.py

from PIL import Image, ImageDraw

# Dictionary mapping graph identifiers to their file paths
graph_paths = {
    'Re': './modules/graphs/Re_graph.png',
    'K': './modules/graphs/K_graph.png',
    'K_fuselage': './modules/graphs/K_fuselage_graph.png',
}

def draw_red_cross_on_graph(image_path):
    """
    Load a graph image, draw a red cross over it, and save the modified image.

    Parameters:
    - image_path: str, path to the original graph image.

    Returns:
    - An Image object with a red cross drawn over it.
    """
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)

            # Get image dimensions
            width, height = img.size

            # Draw two lines (a cross) over the image
            draw.line((0, height // 2, width, height // 2), fill="red", width=2)
            draw.line((width // 2, 0, width // 2, height), fill="red", width=2)

            return img
    except FileNotFoundError:
        print(f"The image {image_path} was not found.")
        return None

def readout_graph(graph_key):
    """
    Load a graph from the graph_paths dictionary, draw a red cross, and display it.

    Parameters:
    - graph_key: str, key of the graph in the graph_paths dictionary.

    Returns:
    - None, but displays the modified image if successful.
    """
    if graph_key in graph_paths:
        image_path = graph_paths[graph_key]
        modified_img = draw_red_cross_on_graph(image_path)
        if modified_img:
            modified_img.show()  # Display the modified image
    else:
        print(f"No graph found for the key '{graph_key}'.")
