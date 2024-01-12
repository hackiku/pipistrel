# import streamlit as st
# import os
# import subprocess


# def map_filename_to_url(filename):
#     base_url = "http://127.0.0.1:8501/"
#     page_name = filename.split('.')[0]  # Assuming filename like '3_3_wing_pg.py'
#     return base_url + page_name


# def main():
#     st.title("Save all LaTeX formulas as images")
#     if st.button("Run Scraper"):
#         run_scraper_for_all_pages()

# def run_scraper_for_all_pages():
#     # List all python files in the 'pages' directory
#     page_files = [f for f in os.listdir('pages') if f.endswith('.py')]

#     # Map filenames to URLs and run scraper for each
#     for file in page_files:
#         url = map_filename_to_url(file)
#         # Assuming your scraper script takes a URL as a command-line argument
#         subprocess.run(["python", "scrape_latex/wip_scraper.py", url])

# if __name__ == "__main__":
#     main()
