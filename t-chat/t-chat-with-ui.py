import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
from langchain.chat_models import ChatOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import threading

load_dotenv()

api_key = os.environ['API_KEY']

chat = ChatOpenAI(
    openai_api_key=api_key
)

memory = ConversationBufferMemory(memory_key="messages", return_messages=True)

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[MessagesPlaceholder(variable_name="messages"),
              HumanMessagePromptTemplate.from_template("{content}")]
)

chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory
)


def process_question():
    content = entry.get()

    # Disable the entry and button during processing
    entry.config(state=tk.DISABLED)
    ask_button.config(state=tk.DISABLED)

    # Show a loading message or spinner
    response_label.config(text="Processing...")

    def run_model():
        try:
            result = chain({"content": content})
            # Update the response label with the model's response
            response_label.config(text=result['text'])
            # Enable the copy button
            copy_button.config(state=tk.NORMAL)
        except Exception as e:
            # Handle errors, for example, display an error message
            response_label.config(text=f"Error: {str(e)}")
        finally:
            # Re-enable the entry and button after processing
            entry.config(state=tk.NORMAL)
            ask_button.config(state=tk.NORMAL)

    # Run the model interaction in a separate thread
    threading.Thread(target=run_model).start()


def copy_to_clipboard():
    response = response_label.cget("text")
    window.clipboard_clear()
    window.clipboard_append(response)
    window.update()  # Update the clipboard
    messagebox.showinfo("Copy", "Response copied to clipboard!")


# Create main window
window = tk.Tk()
window.title("Chat UI")

# Input entry
entry = tk.Entry(window, width=50)
entry.pack(pady=10)

# Button to ask question
ask_button = tk.Button(window, text="Ask Question", command=process_question)
ask_button.pack()

# Label to display responses
response_label = tk.Label(window, text="", wraplength=400)
response_label.pack(pady=10)

# Button to copy response to clipboard
copy_button = tk.Button(window, text="Copy", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack()

# Run the Tkinter event loop
window.mainloop()
