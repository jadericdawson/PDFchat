# PDFchat
By: Jaderic Dawson

## Prerequisites
The application requires Python 3.6+ to run.

## Installation
1. Install Python if not already installed. Detailed instructions for installation can be found [here: Python Installation](https://python.org/installation).
2. Place all files in the same folder.
    - PDFchat.py
    - setup.py
    - requirements.txt
    - README.docx
3. Run the following command:

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
Click the "Open PDF" button and select the PDF files you want to process. You may hold Ctrl and select multiple files. PDF files do not need to be located in the same folder as the Python script, however, reference files will be generated in the same directory as the first selected PDF.
After processing is finished, you can start asking the document(s) questions.

### Chat history
Sometimes Chat History can interfere with querying detailed responses. Use Chat History when you want to ask a series of questions requiring memory. If you want to know information directly from the text, turn Chat history off.

### Group answers
Occasionally you may want to see results separately such as asking for lists or 'each' of something. Deselect "Group answers" in those cases. Alternatively, turn on "Group answers" to output results in paragraph form.

### Save Chat
If you want to save the chat history to a text file, select "Save Chat" then press the "Save" button.

### Reset QA
This button clears the chat history and resubmits the last question. Sometimes you will get a different answer if the chat history is cleared. This is similar to using "Enable Chat History."

### Reset All
Deletes all embeddings, chunks, and text files associated with the original importing of the PDF document(s). These files exist so the same PDF file or series of PDF files can be opened/closed without requiring calls to the OpenAI API, which incurs fees. Use this button if the chat bot is not behaving correctly or errors are encountered.

### AI Creativity
By default AI creativity is set to 1. After opening your PDFs you may slide this bar left or right to a value ranging between 0 and 2 respectively. Lower temperature values will output results more closely matching the text while higher temperature values will impart more randomness to the chat queries, avoid the extremes 0 & 2. The previous question will be automatically executed at the new temperature after releasing the slider.
