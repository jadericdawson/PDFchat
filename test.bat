@echo off

echo Downloading Anaconda3-2023.07-1-Windows-x86_64.exe...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://repo.anaconda.com/archive/Anaconda3-2023.07-1-Windows-x86_64.exe -OutFile Anaconda3-2023.07-1-Windows-x86_64.exe"
start /wait "" Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3


REM Check if Visual Studio already installed
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\SxS\VS7" > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Downloading Visual Studio Installer...
    REM Download Visual Studio Installer with the correct URL
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest https://aka.ms/vs/17/release/vs_community.exe -OutFile vs_installer.exe"

    echo Installing Visual Studio...
    REM Install Visual Studio with the Build Tools workload
    start /wait vs_installer.exe -p --installPath "C:\Path\To\VisualStudio" --add Microsoft.VisualStudio.Workload.VCTools
) else (
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
