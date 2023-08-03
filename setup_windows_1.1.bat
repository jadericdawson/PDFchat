@echo off

REM Define Python version, Installer name and Installation directory
set PYTHON_VERSION=3.11.4
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_PATH=C:\Python%PYTHON_VERSION%

REM Check if Python already installed
where python > nul 2>&1
if %ERRORLEVEL% neq 0 (
    REM Download the Python installer if it doesn't exist
    if not exist %PYTHON_INSTALLER% (
        echo Downloading Python %PYTHON_VERSION% installer...
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER% -OutFile %PYTHON_INSTALLER%"
    )

    REM Install Python (and pip, which is included in the installer)
    echo Installing Python %PYTHON_VERSION%...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%PYTHON_PATH%
) else (
    echo Python is already installed, skipping installation.
)

REM Check if Microsoft Visual C++ Redistributable already installed
REM You can modify the registry key according to the specific version you want to check
reg query "HKLM\SOFTWARE\Classes\Installer\Dependencies\Microsoft.VS.VC_Runtime,version=14.0,amd64" > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Downloading Microsoft Visual C++ Redistributable...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://aka.ms/vs/16/release/vc_redist.x64.exe -OutFile vc_redist.x64.exe"
    echo Installing Microsoft Visual C++ Redistributable...
    start /wait vc_redist.x64.exe /install /quiet /norestart
) else (
    echo Microsoft Visual C++ Redistributable is already installed, skipping installation.
)

REM Temporary add Python and Python Scripts to the PATH. 
SET "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"

REM Python and pip are now installed and added to PATH. 
REM Use pip to install the script's dependencies

echo Installing Python libraries...
pip install textract tiktoken transformers langchain torch tensorflow openai

REM Run your Python script
echo Running your script...
python PDFchat.py

pause
