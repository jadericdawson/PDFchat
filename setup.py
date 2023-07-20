from setuptools import setup, find_packages
import subprocess
import os

# The text of the requirements file
REQUIREMENTS_FILE = "requirements.txt"

subprocess.call(f'pip install -r {REQUIREMENTS_FILE}', shell=True)

setup(
    name="PDFchat_multiPDF_18July2023",
    version="1.0",
    description="A chatbot application for interacting with PDF files",
    url="https://github.com/your-github-username/PDFchat_multiPDF_18July2023",
    author="Your Name",
    author_email="Your Email",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
)
