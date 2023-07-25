from setuptools import setup, find_packages
import subprocess
import os
import platform

# The text of the requirements file
REQUIREMENTS_FILE = "requirements.txt"

# Determine the pip command based on the operating system
if platform.system() == "Windows":
    pip_command = "pip"
elif platform.system() == "Linux":
    pip_command = "pip3"
else:
    raise OSError("Unsupported operating system.")

# Install the required packages using the appropriate pip command
subprocess.call(f'{pip_command} install -r {REQUIREMENTS_FILE}', shell=True)

setup(
    name="PDFchat",
    version="1.0",
    description="A chatbot application for interacting with PDF files",
    url="https://github.com/jadericdawson/PDFchat",
    author="Jaderic Dawson",
    author_email="",
    classifiers=[
        "License :: OSI Approved :: Python Software Foundation License"
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
)
