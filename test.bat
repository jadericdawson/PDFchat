@echo off

REM Define the Miniconda installer filename
set "MINICONDA_INSTALLER=Miniconda3-latest-Windows-x86_64.exe"

REM Check if Miniconda already exists in the current directory
if exist %MINICONDA_INSTALLER% (
    echo Miniconda is already downloaded in the current directory, skipping download and installation.
) else (
    echo Downloading Miniconda3-latest-Windows-x86_64.exe...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://repo.anaconda.com/miniconda/%MINICONDA_INSTALLER% -OutFile %MINICONDA_INSTALLER%"
    start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3


REM Optional: Add Miniconda to the PATH environment variable (uncomment the line below)
REM set "PATH=%UserProfile%\Miniconda3;%UserProfile%\Miniconda3\Scripts;%PATH%"


REM Check if Visual Studio is already installed
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\SxS\VS7" > nul 2>&1
if %ERRORLEVEL% neq 0 (
    REM Visual Studio is not installed, download and install it
    echo Downloading Visual Studio Installer...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://aka.ms/vs/17/release/vs_community.exe -OutFile vs_installer.exe"

    echo Installing Visual Studio...
    start /wait vs_installer.exe -p --installPath "C:\Path\To\VisualStudio" --add Microsoft.VisualStudio.Workload.VCTools
) else (
    REM Visual Studio is already installed, skip the installation
    echo Visual Studio is already installed, skipping installation.
)

REM Temporary add Python and Python Scripts to the PATH.
SET "PATH=%PYTHON_PATH%;%PYTHON_PATH%\Scripts;%PATH%"

REM Install or update Python libraries
echo Installing or updating Python libraries...
pip install --upgrade textract tiktoken transformers langchain torch tensorflow openai

REM Run your Python script
REM echo Running your script...
REM python PDFchat.py

python setup.py install

pause
