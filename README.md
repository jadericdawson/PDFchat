# PDFchat
By: Jaderic Dawson

PDFchat is a compact application designed to facilitate the import of PDF files into a ChatGPT environment. This unique feature enables users to interactively 'converse' with their documents. Ensure that all the materials you wish to reference are opened simultaneously from the same folder for the best experience.

## Prerequisites
The application requires Python 3.6+ to run. 
IMPORTANT: Be sure to copy/paste your OpenAI API key into PDFchat.py before executing anything.

## Installation
1. Install Python if not already installed. Detailed instructions for installation can be found [here: Python Installation](https://python.org/installation) or run the installation scripts below.

### Windows
Download and extract PDFchat.zip directly from Github.  <br />
https://github.com/jadericdawson/PDFchat <br />
- Once downloaded, run "setup_env.bat" <br />
- A warning dialog will appear because you're running a .bat file, run anyway.
- The batch file will check your system and install python, c++, and required dependencies as needed.

### Linux
Run this command in a terminal from the current directory:
```
sudo chmod +x setup_env.sh
sudo ./setup_env.sh
```

2. Organize all the following files within the same directory:
    - PDFchat.py
    - setup.py
    - requirements.txt
    - README.docx
      
3. If you already have Python installed on your system, install the necessary packages, execute the command below:

```
python setup.py install
```

After the initial setup, the PDFchat python file can be copied or moved to any location.
5. Open "PDFchat.py" in a text editor and paste your OpenAI API key between the quotes in this line of the python code.

## Usage
Run the python file with GUI:
```
python PDFchat.py
```
Click on the "Open PDF" button and select the PDF documents you want to convert. For multiple selections, hold Ctrl while selecting. The location of these PDF files need not coincide with the Python script's directory. However, the reference files generated will be stored in the same folder as the first selected PDF. Once the processing concludes, you're ready to ask your document(s) questions!

### Chat history
While Chat History can occasionally hamper extracting detailed responses, it is quite useful when you wish to ask a sequence of interconnected questions that require memory. For direct information retrieval from the text, disable the Chat history.

### Group answers
Depending on your preference, you can choose to see the responses either in a list form or as a paragraph. Deselect "Group answers" for the former or activate "Group answers" for the latter.

### Save Chat
To archive your chat history as a text file, select the "Save Chat" option and then hit the "Save" button.

### Reset QA
Clicking this button will purge the chat history and reissue the previous question. You might receive a different response upon clearing the chat history. This functionality is analogous to the "Enable Chat History" feature.

### Reset All
Use this button to remove all embeddings, chunks, and text files linked with the initial import of the PDF document(s). These files are intended to enable reopening of the same PDF files or a sequence thereof without additional calls to the OpenAI API, which would otherwise incur fees. If the chat bot is malfunctioning or errors have been detected, "Reset All" can be useful.

### AI Creativity
The AI creativity level is preset to 1. After loading your PDFs, you can adjust this setting between 0 and 2 using the provided slider. Lower values generate responses that adhere closely to the text, while higher values introduce more randomness into the chat queries. Avoid using the extreme values of 0 & 2. When you adjust the temperature, the prior question will be automatically resubmitted at the new temperature setting.

