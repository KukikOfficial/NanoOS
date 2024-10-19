import os
import shutil

protected_folders = ["Core", "NanoCore", ".git"]
protected_files = ["FileSystem.py", "README.md", "main.py", "Commands.py", "LICENSE", ".gitignore.txt"]

def move_file(src, dest):
    try:
        shutil.move(src, dest)
        print(f"File {src} moved to {dest}")
    except Exception as e:
        print(f"Error moving file: {e}")

def fcreate(filename):
    if not filename:
        print("Specify the filename after 'touch'")
        return

    if not os.path.exists(filename):
        with open(filename, "w+") as file:
            print(f"File '{filename}' created")
    else:
        print(f"File '{filename}' already exists")


def fdelete(filename):
    if not filename:
        print("Specify the filename after 'delete'")
        return

    if filename in protected_files or filename in protected_folders:
        print(f"'{filename}' is protected and cannot be deleted.")
        return

    if os.path.exists(filename):
        try:
            if os.path.isdir(filename):
                shutil.rmtree(filename)
                print(f"Folder '{filename}' deleted along with its contents")
            else:
                os.remove(filename)
                print(f"File '{filename}' deleted")
        except PermissionError:
            print(f"Permission denied: cannot delete '{filename}'. Check your permissions.")
        except Exception as e:
            print(f"Error when deleting '{filename}': {e}")
    else:
        print(f"File or folder '{filename}' does not exist")


def md(folder_name):
    if folder_name:
        try:
            os.mkdir(folder_name)
            print(f"Folder '{folder_name}' created.")
        except FileExistsError:
            print(f"Folder '{folder_name}' already exists.")
        except Exception as e:
            print(f"Error when creating a folder: {e}")
    else:
        print("Specify the folder name after 'md'")


def rd(folder_name):
    if folder_name in protected_folders:
        print(f"Folder '{folder_name}' is protected and cannot be deleted.")
        return

    if folder_name:
        try:
            shutil.rmtree(folder_name)
            print(f"Folder '{folder_name}' and its contents deleted.")
        except FileNotFoundError:
            print(f"Folder '{folder_name}' does not exist.")
        except PermissionError:
            print(f"Permission denied: cannot delete '{folder_name}'. Check your permissions.")
        except Exception as e:
            print(f"Error when deleting the folder: {e}")
    else:
        print("Specify the folder name after 'rd'")


def ls():
    print("\n".join(os.listdir(".")))


def lsl():
    for item in os.listdir("."):
        fullpath = os.path.join(".", item)
        try:
            print(f"{'d' if os.path.isdir(fullpath) else '-'} "
                  f"{'r' if os.access(fullpath, os.R_OK) else '-'}"
                  f"{'w' if os.access(fullpath, os.W_OK) else '-'} "
                  f"{'x' if os.access(fullpath, os.X_OK) else '-'} {item}")
        except Exception as e:
            print(f"Error accessing '{item}': {e}")


def lsa():
    print("\n".join(os.listdir(".")))


def lslh():
    for item in os.listdir("."):
        fullpath = os.path.join(".", item)
        try:
            size = os.path.getsize(fullpath)
            print(
                f"{size} {'d' if os.path.isdir(fullpath) else '-'} "
                f"{'r' if os.access(fullpath, os.R_OK) else '-'}"
                f"{'w' if os.access(fullpath, os.W_OK) else '-'} "
                f"{'x' if os.access(fullpath, os.X_OK) else '-'} {item}"
            )
        except Exception as e:
            print(f"Error accessing '{item}': {e}")

def cd(folder_name=""):
    if not folder_name:
        print(f"Current directory: {os.getcwd()}")
        return

    if folder_name == "..":
        try:
            os.chdir("..")
            print(f"Changed directory to '{os.getcwd()}'")
        except Exception as e:
            print(f"Error when changing directory: {e}")
    else:
        try:
            os.chdir(folder_name)
            print(f"Changed directory to '{folder_name}'")
            print(f"Current directory: {os.getcwd()}")
        except FileNotFoundError:
            print(f"Folder '{folder_name}' does not exist.")
        except NotADirectoryError:
            print(f"'{folder_name}' is not a directory.")
        except Exception as e:
            print(f"Error when changing directory: {e}")

def hide_folder(folder_name):
    if os.path.exists(folder_name):
        try:
            os.system(f'attrib +h {folder_name}')
            print(f"Folder '{folder_name}' is now hidden.")
        except Exception as e:
            print(f"Error when hiding the folder: {e}")
    else:
        print(f"Folder '{folder_name}' does not exist.")

def unhide_folder(folder_name):
    if os.path.exists(folder_name):
        try:
            os.system(f'attrib -h {folder_name}')
            print(f"Folder '{folder_name}' is now visible.")
        except Exception as e:
            print(f"Error when unhiding the folder: {e}")
    else:
        print(f"Folder '{folder_name}' does not exist.")
