from setuptools import setup, find_packages

setup(
    name="virus_model_streamlit",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit",
        # Other dependencies, if any
    ],
    package_data={
        "virus_viewer_component": ["frontend/*"],
    },
)
