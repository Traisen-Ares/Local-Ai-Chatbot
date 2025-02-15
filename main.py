import subprocess
import sys

REQUIRED_MODULES = ["langchain_ollama", "Ollama", "langchain"]

def install_modules():
    for module in REQUIRED_MODULES:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing missing module: {module}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

install_modules()

import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the questions below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3", temperature=2, top_p=5)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI ChatBot LLAMA 3")
        self.root.geometry("600x700")
        self.root.configure(bg="#2C2F33")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)

        self.chat_window = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="#23272A", fg="white", insertbackground="white",
            font=("Arial", 12), state=tk.DISABLED
        )
        self.chat_window.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.input_frame = tk.Frame(root, bg="#2C2F33")
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)

        self.entry_box = tk.Text(
            self.input_frame, bg="#23272A", fg="white", insertbackground="white", font=("Arial", 12),
            height=1, wrap="word"
        )
        self.entry_box.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")
        self.entry_box.bind("<KeyRelease>", self.adjust_textbox_height)  # Adjust height on typing

        self.send_button = tk.Button(
            self.input_frame, text="➤", bg="#7289DA", fg="white", font=("Arial", 12, "bold"),
            activebackground="#5B6EAD", activeforeground="white", relief=tk.FLAT,
            width=3, command=self.send_message
        )
        self.send_button.grid(row=0, column=1, pady=5, sticky="e")

        self.context = ""

    def send_message(self):
        user_message = self.entry_box.get("1.0", tk.END).strip()
        if not user_message:
            return  

        self.update_chat_window(f"YOU: {user_message}", "right", "#40414F")

        self.entry_box.delete("1.0", tk.END)
        self.adjust_textbox_height()  # Reset height after sending

        result = chain.invoke({"context": self.context, "question": user_message})
        self.update_chat_window(f"BOT: {result}", "left", "#4F545C")

        self.context += f"\nUser: {user_message}\nAI: {result}"
        self.context = self.context[-1000:]

    def adjust_textbox_height(self, event=None):
        num_lines = int(self.entry_box.index("end-1c").split(".")[0])  # Get line count
        self.entry_box.config(height=min(5, num_lines))  # Limit max height to 5 lines

    def update_chat_window(self, message, align, color):
        self.chat_window.config(state=tk.NORMAL)
        tag = f"align_{align}"

        self.chat_window.tag_configure(tag, justify=align, foreground="white", background=color)
        self.chat_window.insert(tk.END, message + "\n", tag)
        self.chat_window.config(state=tk.DISABLED)
        self.chat_window.yview(tk.END)

def main():
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
