from os import environ, remove, path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from time import strftime
from pickle import load, dump
#from glob import glob
from textwrap import wrap
from textract import process
#from transformers import GPT2TokenizerFast
import tiktoken
from transformers import OPENAI_GPT_PRETRAINED_MODEL_ARCHIVE_LIST
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# Define global variables
global chat_history
global temperature_bar
global db
global question
global txt_filenames
global pdf_filenames
global enable_chat_history  # Define enable_chat_history as a global variable

# Initialize global variables
question = None
db = None
txt_filenames = []  # Store one or more selected PDF filenames as txt
pdf_filenames = []  # Store one or more selected PDF filenames
enable_chat_history = False  # Initialize enable_chat_history variable

# Set the initial temperature to 1: qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=temperature_bar), db.as_retriever())
temperature_bar = 1

# Print list of pretrained models available in transformers library
print(OPENAI_GPT_PRETRAINED_MODEL_ARCHIVE_LIST)

#######################################################################################################################################
# Set OpenAI API key
environ["OPENAI_API_KEY"] = "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" #Past OpenAI API key between quotes ""
#######################################################################################################################################

# Function to handle the "Open PDF" button
def open_pdf():
    global pdf_filenames
    # Open a file dialog to select multiple PDF files
    selected_filenames = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not selected_filenames:
        # User cancelled the file selection
        return
    pdf_filenames.extend(selected_filenames)
    
    # Create txt_filenames from pdf_filenames
    global txt_filenames
    txt_filenames = [path.splitext(pdf_filename)[0] + ".txt" for pdf_filename in pdf_filenames]

    # Set the top bar text to display the combined filename(s)
    top_bar_text = "PDF Chat"
    if len(pdf_filenames) == 1:
        top_bar_text += f" - {path.basename(pdf_filenames[0])}"
    elif len(pdf_filenames) > 1:
        top_bar_text += f" - {len(pdf_filenames)} PDF files"
    root.title(top_bar_text)  # Update the title of the main window
    
    # Process the PDF files and setup the chatbot in a separate thread
    Thread(target=process_pdfs, args=(pdf_filenames,)).start()

def reset_qa():
    global qa, db, pdf_filenames, txt_filenames
    if db is None:
        open_pdf()
    else:
        last_question = None  # Initialize last_question variable
        if chat_history:  # Check if chat history is not empty
            last_question = chat_history[-1][0]  # Get the last question from chat history
        chat_history.clear()  # Clear the chat history
        qa = None
        #qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=temperature_bar), db.as_retriever())
        qa = ConversationalRetrievalChain.from_llm(
        ChatOpenAI(temperature=temperature_bar, model='gpt-3.5-turbo'), 
        db.as_retriever())
        chatbox.insert(tk.END, "Chat history cleared.\n\n")
        ask_question(last_question)  # Pass the last question to ask_question function


def update_temperature(event):
    global temperature_bar
    temperature_bar = round(slide_bar.get(), 1)
    chatbox.insert(tk.END, "AI Temperature adjusted and chat history cleared.\n")
    chatbox.insert(tk.END, "Regenerating response to the previous question using the new temperature setting.\n\n")
    temperature_label.config(text=f"AI Creativity (0=less, 2=more): {temperature_bar}.")
    reset_qa()

def reset_process(pdf_filenames):
    global txt_filenames

    try:
        for pdf_filename in pdf_filenames:
            txt_filename = path.splitext(pdf_filename)[0] + ".txt"

            # Remove text file
            if path.isfile(txt_filename):
                remove(txt_filename)

            # Remove chunk file
            chunks_filename = f"{txt_filename.replace('.txt', '')}_chunks.pkl"
            if path.isfile(chunks_filename):
                remove(chunks_filename)

        # Remove the combined text file if it exists
        combined_folder = path.dirname(pdf_filenames[0])
        all_txt_filename = path.join(combined_folder, f"combinedtextfrompdfs_{len(pdf_filenames)}_files.txt")
        if path.isfile(all_txt_filename):
            remove(all_txt_filename)

        # Remove the db file
        db_filename = f"{all_txt_filename.replace('.txt', '')}_db.pkl"
        if path.isfile(db_filename):
            remove(db_filename)

    except FileNotFoundError:
        # Ignore file not found errors
        pass

    # Process the PDF files and setup the chatbot in a separate thread
    Thread(target=process_pdfs, args=(pdf_filenames,)).start()




def process_pdfs(pdf_filenames):
    global embeddings_dict
    global db
    global txt_filenames

    all_chunks = []  # List to store all chunks from multiple PDF files
    text_dict = {}
    # Count the number of PDF files selected
    num_files = len(pdf_filenames)

    # Define the folder path for the combined files
    combined_folder = path.dirname(pdf_filenames[0])

    # Prepare the file paths for the combined text and embeddings files
    all_txt_filename = path.join(combined_folder, f"combinedtextfrompdfs_{num_files}_files.txt")
    embeddings_filename = path.join(combined_folder, f"combinedtextfrompdfs_{num_files}_files_all_embeddings.pkl")

    chatbox.insert(tk.END, "Running...\n")
    print("Running...")

    for pdf_filename in pdf_filenames:
        # 1. Chunking the PDF
        txt_filename = path.splitext(pdf_filename)[0] + ".txt"
        pdf_filename_short = path.basename(pdf_filename)
        txt_filename_short = path.basename(txt_filename)
        # Convert PDF to text using textract
        # Documentation: https://textract.readthedocs.io/en/stable/

        chatbox.insert(tk.END, f"Converting PDF to TXT: {pdf_filename_short}\n")

        # Check if the .txt file already exists
        if not path.isfile(txt_filename):
            doc = process(pdf_filename)

            # Save the converted text to a .txt file
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(doc.decode('utf-8', errors='ignore'))

        # Open the .txt file
        with open(txt_filename, 'r', encoding='utf-8') as f:
            text = f.read()
            chatbox.insert(tk.END, f"Reading text file: {txt_filename_short}\n")

        # Store the text content in the dictionary
        text_dict[pdf_filename] = text

    # Concatenate all text files
    all_text = '\n'.join(text_dict.values())

    # Save the combined text to a file
    with open(all_txt_filename, 'w', encoding='utf-8') as f:
        f.write(all_text)

    # Open the .txt file
    with open(all_txt_filename, 'r', encoding='utf-8') as f:
        text = f.read()
        chatbox.insert(tk.END, f"Reading text file: {all_txt_filename}\n")

    # Create a function to count tokens using GPT2TokenizerFast
    # Documentation: https://huggingface.co/transformers/main_classes/tokenizer.html#transformers.PreTrainedTokenizer
    #tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str) -> int:
        return len(tokenizer.encode(text))

    # Define your desired chunk sizes
    chunk_sizes = [128, 512]  # You can modify this list according to your requirements
    for pdf_filename in pdf_filenames:
        # Create a dictionary to store chunks of different sizes
        chunks_dict = {}

        chunks_filename = f"{pdf_filename.replace('.pdf', '')}_chunks.pkl"

        if path.isfile(chunks_filename):
            # Load chunks from file if it exists
            with open(chunks_filename, 'rb') as f:
                print("Chunks file found. Loading chunks from file...")
                chatbox.insert(tk.END, "Chunks file found. Loading chunks from file...\n")
                chunks_dict = load(f)
        else:
            for size in chunk_sizes:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=size,
                    chunk_overlap=24,
                    length_function=count_tokens,
                )
                chatbox.insert(tk.END, f"Using Text Splitter for chunk size {size}...\n")
                chunks_dict[size] = text_splitter.create_documents([text])

            # Save chunks to file
            with open(chunks_filename, 'wb') as f:
                print("Saving chunks to file...")
                chatbox.insert(tk.END, "Saving chunks to file...\n")
                dump(chunks_dict, f)

        # Concatenate all chunks
        for size, chunks in chunks_dict.items():
            all_chunks += chunks

    # Prepare a filename for the embeddings
    embeddings_filename = f"{all_txt_filename.replace('.txt', '')}_all_embeddings.pkl"
    db_filename = f"{all_txt_filename.replace('.txt', '')}_db.pkl"
    from langchain.vectorstores import FAISS	
    # Check if db file exists, if not generate new embeddings and create db object
    if path.isfile(db_filename):
        # Load db from file if it exists
        with open(db_filename, 'rb') as f:
            print("DB file found. Loading db from file...")
            chatbox.insert(tk.END, "DB file found. Loading db from file...\n")
            db = load(f)
    else:
        print("Generating embeddings and creating FAISS library...")
        chatbox.insert(tk.END, "Generating embeddings and creating FAISS library...\n")
        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        db = FAISS.from_documents(all_chunks, embeddings)
        with open(db_filename, 'wb') as f:
            dump(db, f)

    # Create conversation chain that uses our vectordb as retriever, this also allows for chat history management
    # Documentation: https://langchain.readthedocs.io/en/latest/langchain.chains.html
    global qa
    print(temperature_bar)
    #persona_prompt = "I am a systems engineer for the united states air force tasked with reading, understanding, and teaching the content of air systems handbooks and Air Force instructions. The information I am given is from PDF files."

    #qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=temperature_bar), db.as_retriever())
    qa = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(temperature=temperature_bar, model='gpt-3.5-turbo'), 
    db.as_retriever())

    global chat_history
    chat_history = []

    print("Welcome to PDFchat! Type 'exit' to stop.")
    chatbox.insert(tk.END,"\nWelcome to PDFchat! Type 'exit' to stop.\n\n\n")
    MAX_TOKENS = 1024  # You might want to adjust this based on your specific model

    # After processing the PDF files, enable the "Ask Question" button and entry
    question_entry.config(state=tk.NORMAL)
    ask_button.config(state=tk.NORMAL)
    ask_button.focus_set()
    question_entry.focus_set()

def enter_pressed(event=None):
    # Update the chatbox
    chatbox.insert(tk.END, "...\n\n")
    chatbox.update_idletasks()  # Forces the chatbox to update

    # Get the question from the entry widget
    question = question_entry.get()

    # Call ask_question with the question argument
    ask_question(question)

    # Clear the entry widget
    question_entry.delete(0, tk.END)

# Function to handle the checkbox state change
def enable_chat_history_changed():
    global enable_chat_history
    enable_chat_history = enable_chat_history_var.get()

# Function to handle the "Ask Question" button
def ask_question(question):
    if not question:
        return

    if question.lower() == "exit":
        root.destroy()

    if not enable_chat_history:
        chat_history.clear()  # Clear the chat history


    # Call the update_save_button_state function initially to set the button state
    update_save_button_state()

    global qa
    result = qa({"question": question, "chat_history": chat_history})
    answer = result['answer']
    chat_history.append((question, answer))

    # Display the question in the chatbox
    chatbox.tag_config("user", font=("Helvetica", 12, "bold"))
    chatbox.insert(tk.END, "User: " + question + "\n\n")

    # Display the answer(s) in the chatbox
    chatbox.tag_config("chatbot", font=("Helvetica", 12, "italic"))
    if answer_mode.get() == 0:  # split answers
        answers = answer.split(", ")
        for idx, ans in enumerate(answers):
            chatbox.insert(tk.END, f"Answer({idx+1}): {ans.strip()}\n")
    else:  # group answers
        chatbox.insert(tk.END, f"Answer: {answer.strip()}\n")

    chatbox.insert(tk.END, "\n")
    question_entry.delete(0, tk.END)
    chatbox.see(tk.END)

# Function to handle the "Save Chat" button
def save_chat():
    # Get the chat history from the chatbox
    chat_text = chatbox.get("1.0", tk.END)

    # Extract the base file name from the TXT file path
    base_filenames = [path.basename(txt_filename) for txt_filename in txt_filenames]

    # Append "_CHAT" to the base file names to suggest default file names
    default_filenames = [path.splitext(base_filename)[0] + "_CHAT_HISTORY_" + strftime("_%Y-%m-%d.txt") for base_filename in base_filenames]

    # Open a file dialog to select the save location
    save_filename = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_filenames[0], filetypes=[("Text Files", "*.txt")])

    # Wrap the chat text by inserting line breaks after a certain number of characters
    wrapped_chat_text = wrap_text(chat_text, 80)  # Set the desired line width (e.g., 80 characters)

    # Save the wrapped chat history to a text file
    with open(save_filename, "w", encoding="utf-8") as file:
        file.write(wrapped_chat_text)

    print("Chat saved successfully!")
    chatbox.insert(tk.END, "Chat saved successfully!\n\n")

# Function to wrap text by inserting line breaks after a certain number of characters
def wrap_text(text, width):
    wrapped_lines = []
    lines = text.split("\n")
    for line in lines:
        wrapped_line = "\n".join(wrap(line, width=width))
        wrapped_lines.append(wrapped_line)
    return "\n".join(wrapped_lines)

# Update the state of the "Save Chat" button
def update_save_button_state(event=None):
    if chatbox.get("1.0", tk.END).strip():
        save_button.config(state=tk.NORMAL)
    else:
        save_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root['bg'] = 'linen'
# Set the title
root.title(f"PDF Chat")

# Create a frame for the "Reset" button
top_frame = tk.Frame(root)
top_frame.pack(side="top", fill="x")
top_frame['bg'] = 'linen'

# Create a "Reset QA" button
reset_qa_button = tk.Button(top_frame, font=("Helvetica", 12, "bold"), text="Reset QA", command=reset_qa)
reset_qa_button['bg'] = 'antique white'
reset_qa_button.pack(side="left")

# Create a "Reset" button
reset_button = tk.Button(top_frame, text="Reset All", font=("Helvetica", 12, "bold"), command=lambda: reset_process(pdf_filenames))
reset_button['bg'] = 'antique white'
reset_button.pack(side="left")


# Create a label for the additional text
reset_text = "Note: To reprocess PDF files press 'Reset All.'"
reset_label = tk.Label(top_frame, text=reset_text, font=("Helvetica", 10, "bold"))
reset_label.pack(side="left", padx=10)  # Adjust the padding as desired
reset_label['bg'] = 'linen'

# Create a frame for scale and label
scale_frame = tk.Frame(top_frame, bg='linen')
scale_frame

scale_frame.pack(side='right')
# Create a Scale widget
slide_bar = ttk.Scale(scale_frame, from_=0, to=2, length=200, orient='horizontal', value=1)
slide_bar.grid(row=1, column=0)
# Create a label widget to display the temperature
temperature_label = tk.Label(scale_frame, text=f"AI Creativity (0=less, 2=more): {temperature_bar} ", bg='linen')
temperature_label.grid(row=0, column=0)
# Bind the event to the update_temperature function
slide_bar.bind("<ButtonRelease-1>", update_temperature)

# Create a text widget for the chatbot
chatbox = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 12))
chatbox.pack()

# Create an "Open PDF" button
open_button = tk.Button(root, font=("Helvetica", 12, "bold"), text="Open PDF", command=open_pdf)
open_button['bg'] = 'antique white'
open_button.pack()

# Create an entry widget for the question
question_entry = tk.Entry(root, font=("Helvetica", 12), state=tk.DISABLED, width=50)
question_entry.pack()

#***********
# Create a frame for the checkbox and button
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(side="top", pady=5)
checkbox_frame['bg'] = 'linen'

# Create a checkbox for enabling chat history
enable_chat_history_var = tk.BooleanVar()
enable_chat_history_checkbox = tk.Checkbutton(checkbox_frame, text="Enable Chat History", variable=enable_chat_history_var)
enable_chat_history_checkbox['bg'] = 'linen'
enable_chat_history_checkbox.pack(side="right")
# Define the checkbox variable
enable_chat_history_var = tk.BooleanVar()

# Bind the checkbox state change to the function
enable_chat_history_var.trace("w", enable_chat_history_changed)
#***********

# Create an "Ask Question" button
ask_button = tk.Button(root, font=("Helvetica", 12, "bold"), text="Ask Question", command=enter_pressed, state=tk.DISABLED)
ask_button['bg'] = 'antique white'
ask_button.pack()

# Create a "Save Chat" button
save_button = tk.Button(root, font=("Helvetica", 12, "bold"), text="Save Chat", command=save_chat, state=tk.DISABLED)
save_button['bg'] = 'antique white'
save_button.pack()

# Define the checkbox variable
answer_mode = tk.IntVar()
# Create a Checkbutton widget
toggle_btn = tk.Checkbutton(root, text='Group answers', variable=answer_mode)
# Add the Checkbutton to the root window using pack
toggle_btn.pack()

# Bind the update_save_button_state function to changes in the chatbox
question_entry.bind("<<Modified>>", update_save_button_state)

# Bind the 'Enter' key to the ask_question function
root.bind('<Return>', enter_pressed)

# Start the main loop
root.mainloop()
