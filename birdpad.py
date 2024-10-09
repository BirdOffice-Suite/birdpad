import tkinter as tk
import tkinter.filedialog
import platform
import os
import string
from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter.ttk import Style
from tkinter import scrolledtext
from tkmacosx import Button
from sys import argv
import sys, webbrowser
from spellchecker import SpellChecker

# Initialize logging
logging = False
logs = []

# Initialize the spell checker
spell = SpellChecker()
custom_words = ["BirdPad", "Australorp", "BirdBrush", "BirdOffice", "BirdMenu"]  # Programmatic list of custom words

# Function to strip punctuation
def strip_punctuation(word):
    return word.translate(str.maketrans('', '', string.punctuation))

# File handling functions
def saveas_file():
    try:
        global fname
        fname = tk.filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("HTML files", "*.html"), ("HTM files", "*.htm"), ("Python files", "*.py"),("Arduino C++ files", "*.ino"), ("All files", "*.*")])
        log(f"Save file to {fname}.")
        with open(fname, "w") as f:
            f.write(text_box.get("1.0", tk.END)[0:-1])
        showinfo("BirdPad", "File saved successfully!")
    except (AttributeError, FileNotFoundError):
        showerror(title='BirdPad', message="File not found or failed to save.")
        log("File not found or failed to save.")
    except NameError:
        pass
    return fname

def save_file():
    try:
        global fname
        if fname:
            with open(fname, 'w', encoding='utf-16') as f:
                f.write(text_box.get("1.0", tk.END)[0:-1])
            showinfo("BirdPad", "File saved successfully")
    except NameError:
        fname = saveas_file()

def load_file(fname=None):
    if fname:
        log(f"Load file from {fname}.")
        try:
            with open(fname, 'r') as f:
                text_box.delete("1.0", tk.END)
                text_box.insert("1.0", f.read())
        except UnicodeDecodeError:
            showerror(title='BirdPad', message="This file is not a text document and cannot be read by BirdPad.")
            log("This file is not a text document and cannot be read by BirdPad.")
        except FileNotFoundError:
            showerror(title='BirdPad', message="File not found.")
            log("File not found.")
    else:
        try:
            fname = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("HTML files", "*.html"), ("HTM files", "*.htm"), ("Python files", "*.py"), ("Arduino C++ files", "*.ino"), ("All files", "*.*")])
            log(f"Load file from {fname}.")
            with open(fname, 'r') as f:
                text_box.delete("1.0", tk.END)
                text_box.insert("1.0", f.read())
        except UnicodeDecodeError:
            showerror(title='BirdPad', message="This file is not a text document and cannot be read by BirdPad.")
            log("This file is not a text document and cannot be read by BirdPad.")
        except FileNotFoundError:
            if fname:
                showerror(title='BirdPad', message="File not found.")
                log("File not found.")

def quit_bpad():
    log(f"Ask if app should be closed.")
    answer = askyesno(title='Quit BirdPad', message='Are you sure that you want to quit?')
    if answer:
        window.destroy()

def resource_path(relative_path):
    log(f"Get resource from {relative_path}.")
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_updates():
    log(f"Ask if app should open browser.")
    answer = askyesno(title='BirdOffice Suite', message='Open browser to download BirdOffice?')
    if answer:
        webbrowser.open_new_tab("https://mojavesoft.net/birdoffice/")

def log(txt):
    print(txt)
    logs.append(txt)

# Spell check function
def check_spelling(event=None):
    text_content = text_box.get("1.0", tk.END)
    words = text_content.split()
    text_box.tag_remove("misspelled", "1.0", tk.END)
    
    for word in words:
        stripped_word = strip_punctuation(word)
        if stripped_word and spell.unknown([stripped_word]) and stripped_word not in custom_words:
            start_idx = f"1.0 + {text_content.index(word)}c"
            end_idx = f"{start_idx} + {len(word)}c"
            text_box.tag_add("misspelled", start_idx, end_idx)

# Add custom word function (optional)
def add_custom_word(word):
    if word:
        custom_words.append(word)  # Add word to programmatic custom word list

# Tkinter setup
window = tk.Tk()
window.title('BirdPad 24.10 (Amazing Australorp)')
window.geometry("700x700")
window.minsize(width=0, height=500)

photo = tk.PhotoImage(file=resource_path('birdpad.png'))
window.wm_iconphoto(False, photo)

# Textbox with spell checking
text_box = scrolledtext.ScrolledText(wrap="none", relief="sunken", undo=True)
text_box.pack(expand=True, fill='both')
text_box.tag_configure("misspelled", foreground="red", underline=True)
text_box.bind('<KeyRelease>', check_spelling)

# Buttons for file handling and other actions
if platform.system() == "Darwin" or "--macos" in sys.argv:
    log("[DEBUG] Using macOS-optimized interface.")
    saveas = Button(window, text="Save", command=saveas_file)
    load = Button(window, text="Load", command=load_file)
    quit_birdpad = Button(window, text="Quit", bg='red', command=quit_bpad, borderless=0)
    birdpad_credits = Button(window, text="Get updates!", bg='orange', command=get_updates, borderless=0)
else:
    log("[DEBUG] Using default interface.")
    saveas = tk.Button(window, text="Save", command=saveas_file)
    load = tk.Button(window, text="Load", command=load_file)
    quit_birdpad = tk.Button(window, text="Quit", bg='red', command=quit_bpad)
    birdpad_credits = tk.Button(window, text="Try out BirdOffice!", bg='orange', command=get_updates)

saveas.pack(side=tk.LEFT, expand=True, fill='both')
load.pack(side=tk.LEFT, expand=True, fill='both')
quit_birdpad.pack(side=tk.RIGHT, expand=True, fill='both')
birdpad_credits.pack(side=tk.RIGHT, expand=True, fill='both')

# Initial text
text_box.insert(tk.END, '''Thanks for installing BirdPad 24.10 Amazing Australorp!

For more software like this, click the "Try out BirdOffice!" button and check out
awesome new programs like BirdBrush and BirdMenu!''')

if len(argv) > 1 and not argv[1] == "--log" and not argv[1] == "--macos":
    load_file(argv[1])

if "--log" in argv:
    logging = True
    
window.mainloop()

# Log save if logging enabled
if logging:
    log_file = open("birdpad.log", "a")
    log_file.write("\n".join(logs))
    log_file.write("\n")
    log_file.close()
