import tkinter as tk
from tkinter import filedialog, messagebox, Menu, simpledialog, ttk
import os
from FileSystem import fcreate, fdelete, md, rd


class FileExplorer(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("File Explorer")
        self.geometry("800x600")

        self.path_var = tk.StringVar()
        self.path_var.set(os.getcwd())

        self.path_frame = tk.Frame(self)
        self.path_frame.pack(padx=10, pady=5, fill=tk.X)

        self.path_entry = tk.Entry(self.path_frame, textvariable=self.path_var, width=60)
        self.path_entry.pack(side=tk.LEFT, padx=10, pady=5)

        self.browse_button = tk.Button(self.path_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.back_button = tk.Button(self.path_frame, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("name", "type", "size"), show="headings")
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.update_file_list()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_var.set(directory)
            self.update_file_list()

    def go_back(self):
        current_path = self.path_var.get()
        parent_path = os.path.dirname(current_path)
        self.path_var.set(parent_path)
        self.update_file_list()

    def update_file_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        path = self.path_var.get()
        try:
            for item in os.listdir(path):
                fullpath = os.path.join(path, item)
                if os.path.isdir(fullpath):
                    self.tree.insert("", "end", values=(item, "Folder", ""))
                else:
                    size = os.path.getsize(fullpath)
                    self.tree.insert("", "end", values=(item, "File", f"{size} bytes"))
        except Exception as e:
            messagebox.showerror("Error", f"Error accessing directory: {e}")

    def on_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            path = os.path.join(self.path_var.get(), self.tree.item(item, "values")[0])
            if os.path.isdir(path):
                self.path_var.set(path)
                self.update_file_list()

    def show_context_menu(self, event):
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Create File", command=self.create_file)
        context_menu.add_command(label="Create Folder", command=self.create_folder)
        context_menu.add_command(label="Delete File", command=self.delete_file)
        context_menu.add_command(label="Delete Folder", command=self.delete_folder)
        context_menu.post(event.x_root, event.y_root)

    def create_file(self):
        filename = simpledialog.askstring("Input", "Enter the filename:")
        if filename:
            fcreate(os.path.join(self.path_var.get(), filename))
            self.update_file_list()

    def create_folder(self):
        foldername = simpledialog.askstring("Input", "Enter the folder name:")
        if foldername:
            md(os.path.join(self.path_var.get(), foldername))
            self.update_file_list()

    def delete_file(self):
        filename = simpledialog.askstring("Input", "Enter the filename:")
        if filename:
            confirmation = messagebox.askyesno("Confirm Delete",
                                               f"Are you sure you want to delete the file '{filename}'?")
            if confirmation:
                fdelete(os.path.join(self.path_var.get(), filename))
                self.update_file_list()

    def delete_folder(self):
        foldername = simpledialog.askstring("Input", "Enter the folder name:")
        if foldername:
            confirmation = messagebox.askyesno("Confirm Delete",
                                               f"Are you sure you want to delete the folder '{foldername}'?")
            if confirmation:
                rd(os.path.join(self.path_var.get(), foldername))
                self.update_file_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    FileExplorer(root)
    root.mainloop()
