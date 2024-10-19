import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, Menu, PhotoImage, Toplevel
from explorer import FileExplorer
from nano_draft import NanoDraft
from FileSystem import fcreate, fdelete, md, rd

class DesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NanoCore Desktop")
        self.geometry("1024x768")
        self.configure(bg='sky blue')
        self.icons_dir = "icons/"

        self.icons = {
            "File Explorer": self.icons_dir + "file_explorer_icon.png",
            "NanoDraft": self.icons_dir + "nanodraft_icon.png",
            "Quit": self.icons_dir + "quit_icon.png",
            "Start": self.icons_dir + "start_icon.png"
        }

        self.icon_positions = []
        self.load_desktop_icons()

        self.taskbar = tk.Frame(self, bg='gray', height=30)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        start_image = PhotoImage(file=self.icons["Start"])
        self.start_button = tk.Button(self.taskbar, image=start_image, command=self.show_start_menu, bg="gray", relief="flat")
        self.start_button.image = start_image
        self.start_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.quit_button = tk.Button(self.taskbar, text="Quit", command=self.quit_app, bg="red", fg="white", height=1)
        self.quit_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.process_buttons = {}
        self.open_windows = {}

        self.bind("<Button-3>", self.show_context_menu)

        self.create_icon("File Explorer", self.open_file_explorer, 50, 50)
        self.create_icon("NanoDraft", self.open_nano_draft, 150, 50)

        self.quit_button.destroy()

    # Обновление метода show_start_menu
    def show_start_menu(self):
        start_menu = Toplevel(self)
        start_menu.title("Start Menu")
        start_menu.geometry(
            "200x300+{}+{}".format(self.start_button.winfo_rootx(), self.start_button.winfo_rooty() - 200))
        start_menu.transient(self)
        start_menu.grab_set()

        icons_frame = tk.Frame(start_menu)
        icons_frame.pack(expand=True, fill=tk.BOTH)

        # Создадим отдельные иконки для меню "Пуск"
        file_explorer_image = PhotoImage(file=self.icons_dir + "start_file_explorer_icon.png").subsample(2, 2)
        nanodraft_image = PhotoImage(file=self.icons_dir + "start_nanodraft_icon.png").subsample(2, 2)

        file_explorer_button = tk.Button(icons_frame, image=file_explorer_image, command=self.open_file_explorer)
        file_explorer_button.image = file_explorer_image  # Чтобы изображение не удалялось сборщиком мусора
        file_explorer_button.grid(row=0, column=0, padx=10, pady=10)

        nanodraft_button = tk.Button(icons_frame, image=nanodraft_image, command=self.open_nano_draft)
        nanodraft_button.image = nanodraft_image  # Чтобы изображение не удалялось сборщиком мусора
        nanodraft_button.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(icons_frame, text="File Explorer").grid(row=1, column=0)
        tk.Label(icons_frame, text="NanoDraft").grid(row=1, column=1)

        tk.Button(icons_frame, text="Quit", command=self.quit_app, bg="red", fg="white").grid(row=2, column=0,
                                                                                              columnspan=2, pady=10)

    # Обновление метода create_icon
    def create_icon(self, text, command, x, y):
        frame = tk.Frame(self, width=100, height=100, bg='sky blue', highlightbackground="black", highlightthickness=1)
        frame.place(x=x, y=y)
        icon_image = PhotoImage(
            file=self.icons.get(text, self.icons["File Explorer"]))  # Вернуть исходный размер иконок
        button = tk.Button(frame, image=icon_image, text=text, compound="top", command=command, bg='light gray',
                           width=80, height=80)
        button.image = icon_image
        button.pack()
        self.icon_positions.append((text, x, y))
        self.save_desktop_icons()  # Save icons after creation
        self.update()  # Force the GUI to update to show the new icon

    # Обновление метода create_file_on_desktop
    def create_file_on_desktop(self):
        filename = simpledialog.askstring("Input", "Enter the filename:")
        if filename:
            fcreate(filename)
            x, y = self.get_next_icon_position()
            self.create_icon(filename, lambda: None, x, y)  # Появление на рабочем столе новой иконки

    # Обновление метода create_folder_on_desktop
    def create_folder_on_desktop(self):
        foldername = simpledialog.askstring("Input", "Enter the folder name:")
        if foldername:
            md(foldername)
            x, y = self.get_next_icon_position()
            self.create_icon(foldername, lambda: None, x, y)  # Появление на рабочем столе новой иконки

    # Добавление метода get_next_icon_position
    def get_next_icon_position(self):
        base_x, base_y = 50, 100
        offset = 100
        num_icons = len(self.icon_positions)
        return base_x + (num_icons % 10) * offset, base_y + (num_icons // 10) * offset

    def load_desktop_icons(self):
        try:
            with open("desktop_icons.txt", "r") as f:
                for line in f:
                    icon_info = line.strip().split(',')
                    name, x, y = icon_info[0], int(icon_info[1]), int(icon_info[2])
                    self.create_icon(name, lambda: None, x, y)
        except FileNotFoundError:
            pass  # No saved icons found

    def save_desktop_icons(self):
        with open("desktop_icons.txt", "w") as f:
            for name, x, y in self.icon_positions:
                f.write(f"{name},{x},{y}\n")

    def show_context_menu(self, event):
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Create File", command=self.create_file_on_desktop)
        context_menu.add_command(label="Create Folder", command=self.create_folder_on_desktop)
        context_menu.add_command(label="Delete File", command=self.delete_file_from_desktop)
        context_menu.add_command(label="Delete Folder", command=self.delete_folder_from_desktop)
        context_menu.post(event.x_root, event.y_root)

    def delete_file_from_desktop(self):
        filename = simpledialog.askstring("Input", "Enter the filename:")
        if filename:
            confirmation = messagebox.askyesno("Confirm Delete",
                                               f"Are you sure you want to delete the file '{filename}'?")
            if confirmation:
                fdelete(filename)
                self.remove_icon_from_desktop(filename)

    def delete_folder_from_desktop(self):
        foldername = simpledialog.askstring("Input", "Enter the folder name:")
        if foldername:
            confirmation = messagebox.askyesno("Confirm Delete",
                                               f"Are you sure you want to delete the folder '{foldername}'?")
            if confirmation:
                rd(foldername)
                self.remove_icon_from_desktop(foldername)

    def launch_process(self, command, name):
        if name in self.open_windows:
            self.open_windows[name].deiconify()
            self.open_windows[name].lift()
        else:
            window = command()
            if window:
                self.open_windows[name] = window
                process_button = tk.Button(self.taskbar, text=name, command=lambda: self.show_window(name))
                process_button.pack(side=tk.LEFT, padx=5, pady=5)
                self.process_buttons[name] = process_button

    def show_window(self, name):
        if name in self.open_windows:
            window = self.open_windows[name]
            window.deiconify()
            window.lift()

    def open_file_explorer(self):
        explorer = FileExplorer(self)
        explorer.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window("File Explorer", explorer))
        return explorer

    def open_nano_draft(self):
        filename = simpledialog.askstring("Input", "Enter the filename:")
        if filename:
            draft = NanoDraft(self, filename)
            draft.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window("NanoDraft", draft))
            return draft
        return None

    def remove_icon_from_desktop(self, name):
        for i, (icon_name, x, y) in enumerate(self.icon_positions):
            if icon_name == name:
                self.icon_positions.pop(i)
                break
        self.save_desktop_icons()
        self.update()  # Force the GUI to update to remove the icon visually

    def on_double_click(self, event):
        item = self.tree.selection()
        if item:
            item = item[0]
            path = os.path.join(self.path_var.get(), self.tree.item(item, "values")[0])
            if os.path.isdir(path):
                self.path_var.set(path)
                self.update_file_list()
            else:
                # Open File Explorer in the directory of the double-clicked file
                self.master.open_file_explorer()

    def on_close_window(self, name, window):
        window.withdraw()
        if name in self.process_buttons:
            self.process_buttons[name].destroy()
            del self.process_buttons[name]
            del self.open_windows[name]

    def quit_app(self):
        self.save_desktop_icons()
        self.quit()


if __name__ == "__main__":
    app = DesktopApp()
    app.mainloop()
