#!/bin/bash
### may need to check if pip is installed

# Define Python version and Installation directory
PYTHON_VERSION=3.11.4
PYTHON_INSTALLER=python-${PYTHON_VERSION}-amd64.exe
PYTHON_PATH=/opt/python${PYTHON_VERSION}

# Download the Python installer if it doesn't exist
if [ ! -f "${PYTHON_INSTALLER}" ]; then
    echo "Downloading Python ${PYTHON_VERSION} installer..."
    wget https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_INSTALLER}
fi

# Install Python (and pip, which is included in the installer)
echo "Installing Python ${PYTHON_VERSION}..."
chmod +x ${PYTHON_INSTALLER}
./${PYTHON_INSTALLER} --prefix=${PYTHON_PATH} --silent --include-pip

# Update PATH to include the new Python installation
echo "Updating PATH..."
export PATH="${PYTHON_PATH}/bin:${PATH}"

# Python and pip are now installed and added to PATH. 
# Use pip to install the script's dependencies
echo "Installing Python libraries..."
pip install textract tiktoken transformers langchain torch tensorflow python3-tk

# Run your Python script
echo "Running your script..."
python3 PDFchat.py
