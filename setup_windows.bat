@echo off

REM Define Python version, Installer name and Installation directory
set PYTHON_VERSION=3.11.4
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_PATH=C:\Python%PYTHON_VERSION%

REM Download the Python installer if it doesn't exist
if not exist %PYTHON_INSTALLER% (
    echo Downloading Python %PYTHON_VERSION% installer...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER% -OutFile %PYTHON_INSTALLER%"
)

REM Install Python (and pip, which is included in the installer)
echo Installing Python %PYTHON_VERSION%...
start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON_PATH%

REM Download and install Microsoft Visual C++ Redistributable
echo Downloading Microsoft Visual C++ Redistributable...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile vc_redist.x64.exe"
echo Installing Microsoft Visual C++ Redistributable...
start /wait vc_redist.x64.exe /install /quiet /norestart

REM Temporary add Python and Python Scripts to the PATH. 
SET "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"

REM Python and pip are now installed and added to PATH. 
REM Use pip to install the script's dependencies

echo Installing Python libraries...
pip install textract tiktoken transformers langchain torch tensorflow

REM Run your Python script
REM echo Running your script...
REM python PDFchat.py
echo Remember to copy and paste your OpenAI API into PDFchat.py...
pause
