import random
from FileSystem import fcreate, fdelete, md, rd, ls, lsl, lsa, lslh, cd, hide_folder, unhide_folder
from System.nano_draft import edit_file, read_file

def help_menu():
    print("""
Help menu:
help - this menu
random - generating random number
shutdown - shutdown os
touch <filename> - create a new file
edit <filename> - edit an existing file
read <filename> - read an existing file
delete - delete a file or folder
md <foldername> - create a new directory
rd <foldername> - remove a directory and its contents
ls - list all files and directories
lsl - list all files and directories with details
lsa - list all files and directories including hidden
lslh - list all files and directories with details and sizes
cd <foldername> - change directory
hide <foldername> - hide a folder
unhide <foldername> - unhide a folder
Draft <filename> - open NanoDraft editor
""")

def command_list():
    userInp = input(">")
    if userInp == "help":
        help_menu()
    elif userInp == "random":
        random_int = random.randint(0, 327679736)
        print(random_int)
    elif userInp == "shutdown":
        exit()
    elif userInp.startswith("touch"):
        filename = userInp[6:].strip()
        if not filename:
            print("Specify the filename after 'touch'")
        else:
            fcreate(filename)
    elif userInp.startswith("edit"):
        filename = userInp[5:].strip()
        edit_file(filename)
    elif userInp.startswith("read"):
        filename = userInp[5:].strip()
        read_file(filename)
    elif userInp.startswith("delete"):
        filename = userInp[7:].strip()
        if not filename:
            print("Specify the filename after 'delete'")
        else:
            fdelete(filename)
    elif userInp.startswith("md"):
        folder_name = userInp[3:].strip()
        md(folder_name)
    elif userInp.startswith("rd"):
        folder_name = userInp[3:].strip()
        rd(folder_name)
    elif userInp == "ls":
        ls()
    elif userInp == "lsl":
        lsl()
    elif userInp == "lsa":
        lsa()
    elif userInp == "lslh":
        lslh()
    elif userInp.startswith("cd"):
        folder_name = userInp[3:].strip()
        cd(folder_name)
    elif userInp.startswith("hide"):
        folder_name = userInp[5:].strip()
        hide_folder(folder_name)
    elif userInp.startswith("unhide"):
        folder_name = userInp[7:].strip()
        unhide_folder(folder_name)
    elif userInp.startswith("Draft"):
        filename = userInp[6:].strip()
        edit_file(filename)
    else:
        print("Unknown command. Type 'help' for a list of commands.")
