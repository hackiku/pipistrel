from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome and Selenium options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Open the Streamlit app
driver.get('http://localhost:8501')  # Replace with your Streamlit app URL

# Wait for the element to be loaded
wait = WebDriverWait(driver, 10)
katex_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "katex-display")))

# Take a screenshot of the LaTeX element
katex_element.screenshot('latex_formula.png')

# Close the driver
driver.quit()
