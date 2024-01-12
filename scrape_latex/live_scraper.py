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
driver.get('https://pipistrel.streamlit.app/')  # Replace with your Streamlit app URL

# Wait for the page to load and for LaTeX to render
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "katex-html")))
# wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "katex-html")))

# Find all LaTeX elements
katex_elements = driver.find_elements(By.CLASS_NAME, "katex-html")

# Loop through each LaTeX element and save a screenshot
for index, element in enumerate(katex_elements):
    # Inject CSS to adjust the display and add custom padding
    custom_css = "display: inline-block; padding: 3px; box-sizing: border-box;"
    driver.execute_script(f"arguments[0].setAttribute('style', '{custom_css}')", element)

    # Take the screenshot and save it
    filename = os.path.join(latex_dir, f'latex_{index}.png')
    element.screenshot(filename)

# Quit the driver
driver.quit()

print(f"Images saved to {latex_dir}")