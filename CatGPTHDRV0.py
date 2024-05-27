import os
import time
from openai import OpenAI
import tkinter as tk
from threading import Timer

os.environ["OPENAI_API_KEY"] = "lm-studio"
client = OpenAI(base_url="http://localhost:1234/v1")

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CATGPT Terminal 1.0.X.X [C] - Local Server 1.0 [C] Flames Labs 20XX")
        self.geometry("800x600")
        self.resizable(False, False)
        self.create_widgets()
        self.init_chat_history()
        self.start_recall_timer()
        self.chat_history_cache = []

    def create_widgets(self):
        self.chat_history = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.user_input = tk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.LEFT, padx=(10, 0))

        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.output_window = tk.Text(self, wrap=tk.WORD, state=tk.DISABLED)
        self.output_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def init_chat_history(self):
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "CATGPT: Hello! I'm CATGPT. Share your prompt, and I'll generate a response showcasing my capabilities!\n\n")
        self.chat_history.configure(state=tk.DISABLED)

    def send_message(self):
        user_prompt = self.user_input.get()
        self.user_input.delete(0, tk.END)
        self.update_chat_history(f"User: {user_prompt}\n\n")
        self.chat_history_cache.append(f"User: {user_prompt}\n\n")

        ai_output = self.get_ai_output(f"User: {user_prompt}\nCATGPT:")
        self.update_chat_history(f"CATGPT: {ai_output}\n\n")
        self.update_output_window(user_prompt, ai_output)

    def get_ai_output(self, prompt):
        try:
            completion = client.completions.create(
                model="LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return completion.choices[0].text.strip()
        except Exception as e:
            return f"Sorry, I encountered an error while processing your prompt: {str(e)}"

    def update_chat_history(self, message):
        self.chat_history.configure(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message)
        self.chat_history.configure(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def update_output_window(self, user_prompt, ai_output):
        self.output_window.configure(state=tk.NORMAL)
        self.output_window.delete('1.0', tk.END)
        self.output_window.insert(tk.END, f"User Prompt:\n{user_prompt}\n\nCATGPT Output:\n{ai_output}")
        self.output_window.configure(state=tk.DISABLED)

    def start_recall_timer(self):
        self.recall_timer = Timer(180, self.recall_prompt)
        self.recall_timer.start()

    def recall_prompt(self):
        recent_history = "\n".join(self.chat_history_cache[-3:])
        if recent_history:
            recall_prompt = f"What were the key points discussed in the last 3 minutes? {recent_history}"
            recall_output = self.get_ai_output(recall_prompt)
            self.update_chat_history(f"CATGPT Recall: {recall_output}\n\n")
            self.update_output_window(recall_prompt, recall_output)
        self.start_recall_timer()

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
