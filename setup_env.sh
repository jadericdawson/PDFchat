#!/bin/bash

# Name of the virtual environment
VENV_NAME="pdfchat_venv"

# Check if the virtual environment already exists
if [ ! -d "$VENV_NAME" ]; then
    # Create a new virtual environment
    python3 -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

# Install openai package
pip3 install openai

# Install langchain package
pip3 install langchain

# Run setup.py to install your package
python3 setup.py install

python3 PDFchat.py

# Keep the virtual environment active after the script finishes
exec bash

