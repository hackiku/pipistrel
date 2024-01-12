from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Setup Chrome and Selenium options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--start-maximized")  # Start maximized to capture full elements
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Set up directory for saving images
latex_dir = 'latex_renders'
os.makedirs(latex_dir, exist_ok=True)

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Open the Streamlit app
driver.get('http://localhost:8501')  # Replace with your Streamlit app URL

# Wait for the page to load and for LaTeX to render
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "katex-display")))

# Find all LaTeX elements
latex_elements = driver.find_elements(By.CLASS_NAME, "katex-html")

# Loop through each LaTeX element and save a screenshot
for index, element in enumerate(latex_elements):
    # Add some padding to the element for the screenshot
    driver.execute_script("arguments[0].style='padding:3px;'", element)
    
    # Define the filename for the screenshot
    filename = os.path.join(latex_dir, f'latex_{index}.png')
    
    # Take the screenshot and save it
    element.screenshot(filename)

# Quit the driver
driver.quit()

print(f"Images saved to {latex_dir}")
