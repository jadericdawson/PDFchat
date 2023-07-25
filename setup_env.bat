@echo off

rem Name of the virtual environment
set VENV_NAME=pdfchat_venv

rem Check if the virtual environment already exists
if not exist %VENV_NAME% (
    rem Create a new virtual environment
    python -m venv %VENV_NAME%
)

rem Activate the virtual environment
call %VENV_NAME%\Scripts\activate

rem Install dependencies from requirements.txt
pip install -r requirements.txt

rem Run setup.py to install your package
python setup.py install

