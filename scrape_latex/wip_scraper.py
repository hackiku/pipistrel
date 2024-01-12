from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Define the base URL and directory for renders
base_url = "http://127.0.0.1:8501"
renders_dir = "./scrape_latex/latex_renders"  # Adjusted to relative path

# Define the mapping of Streamlit page paths to folder names
page_to_folder_map = {
    "/": "2_home",
    "/2_airfoil": "3_airfoil",
    "/3_wing_pg": "4_wing",
    # Add more mappings as needed...
}

# Setup Chrome and Selenium options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--start-maximized")  # Start maximized to capture full elements
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Loop through each page and its corresponding folder
for page_path, folder_name in page_to_folder_map.items():
    # Construct the full URL and folder path
    url = f"{base_url}{page_path}"
    folder_path = os.path.join(renders_dir, folder_name)
    
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Folder does not exist: {folder_path}")
        continue
    
    # Navigate to the page
    driver.get(url)
    
    # Wait for the LaTeX to render
    wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "katex-html")))
    
    # Find all LaTeX elements
    katex_elements = driver.find_elements(By.CLASS_NAME, "katex-html")
    
    # Save screenshots of LaTeX elements
    for index, element in enumerate(katex_elements):
        filename = os.path.join(folder_path, f'latex_{index}.png')
        element.screenshot(filename)
    
    print(f"Images saved to {folder_path}")

# Quit the driver
driver.quit()
