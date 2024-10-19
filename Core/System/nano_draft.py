import tkinter as tk
from tkinter import Tk, Canvas, Toplevel
from tkinter import scrolledtext, simpledialog

class RoundedWindow(Toplevel):
    def __init__(self, master=None, **kwargs):
        Toplevel.__init__(self, master, **kwargs)
        self.wm_overrideredirect(True)  # убираем стандартный заголовок окна
        self.canvas = Canvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_oval(10, 10, 50, 50, fill="blue")  # пример овала
        self.canvas.create_rectangle(50, 50, 100, 100, fill="red")

    def show(self):
        self.update_idletasks()
        self.after(10, lambda: self.wm_deiconify())


class NanoDraft(tk.Toplevel):
    def __init__(self, master, filename=""):
        super().__init__(master)
        self.title("NanoDraft")
        self.geometry("800x600")
        self.master = master

        if not filename:
            filename = simpledialog.askstring("Input", "Enter the filename:")
            if not filename:
                self.destroy()
                self.master.remove_process_button("NanoDraft")
                return

        self.filename = filename

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=30)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.save_button = tk.Button(self, text="Save", command=self.save_file)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.exit_button = tk.Button(self, text="Exit", command=self.on_close)
        self.exit_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.load_file()

    def load_file(self):
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
                self.text_area.insert(tk.END, content)
        except FileNotFoundError:
            print(f"File '{self.filename}' does not exist. Creating a new file.")
        except Exception as e:
            print(f"Error loading file: {e}")

    def save_file(self):
        content = self.text_area.get("1.0", tk.END)
        try:
            with open(self.filename, 'w') as file:
                file.write(content)
            print(f"File '{self.filename}' saved.")
        except Exception as e:
            print(f"Error saving file: {e}")

    def on_close(self):
        self.destroy()
        self.master.remove_process_button("NanoDraft")
