import tkinter.filedialog, platform, os, string, math
from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter import scrolledtext
from tkmacosx import Button
from sys import argv
import sys, webbrowser
from spellchecker import SpellChecker
import tkinter as tk
from requests import get, ConnectionError

# START DONATION CODE
#from tkinter import messagebox
#from random import randint
#import sys


#if randint(0,3) == 1 and not "--no-popup" in sys.argv:
    #showinfo("BirdOffice 24.11", "Thank you for downloading BirdPad! If you like this software, make sure to donate at www.mojavesoft.net/donate/!")


# END DONATION CODE


# Initialize logging
logging = False
logs = []

# Initialize the spell checker
spell = SpellChecker()
custom_words = ["BirdPad", "Australorp", "BirdBrush", "BirdOffice", "BirdMenu", "BirdPad", "Brahma", "mojavesoft", "mojaveland"]  # Programmatic list of custom words

# Function to strip punctuation
def strip_punctuation(word):
    return word.translate(str.maketrans('', '', string.punctuation))

# File handling functions
def saveas_file():
    try:
        global fname
        fname = tk.filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("HTML files", "*.html"), ("HTM files", "*.htm"), ("Python files", "*.py"), ("Arduino C++ files", "*.ino"), ("All files", "*.*")])
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
        # Check if the stripped word is in custom_words case-insensitively
        if stripped_word and spell.unknown([stripped_word]) and stripped_word.lower() not in [w.lower() for w in custom_words]:
            start_idx = f"1.0 + {text_content.index(word)}c"
            end_idx = f"{start_idx} + {len(word)}c"
            text_box.tag_add("misspelled", start_idx, end_idx)

# Autocorrect function
updated = False

def autocorrect():
    global updated

    if not updated:
        answer = askyesno('BirdPad', "It looks like you're using autocorrect. Would you like to download the extended dictionary via the Internet?")

    else:
        answer = False
        
    if answer:
         try:
            global custom_words
            print("[DEBUG] Updating spellcheck from API...")

            ypages = get("https://mojavesoft.net/api/v1/birdpad/ypages.txt").text.split("\n")

            for i in ypages:
                custom_words.extend(get(i).text.split("\n"))
            #custom_words = list(set(custom_words))
            showinfo("BirdPad", f"Downloaded extended dictionary! ({math.floor(len(custom_words)/1000)}k entries)")

         except ConnectionError:
            showerror("BirdPad", "mojavesoft.net is not available. Try again in a couple hours.")

            
         except Exception as e:
            showerror("BirdPad", e)
            print(e)

         updated = True
         print("[DEBUG] Spellcheck update complete")

    
        
    text_content = text_box.get("1.0", tk.END)
    corrected_text = []
    
    word = ""
    for char in text_content:
        if char in string.whitespace:  # Preserve whitespaces (spaces, newlines, etc.)
            if word:
                stripped_word = strip_punctuation(word)
                # Check if the stripped word is in custom_words case-insensitively
                if stripped_word and spell.unknown([stripped_word]) and stripped_word.lower() not in [w.lower() for w in custom_words]:
                    # Correct the word
                    corrected_word = spell.candidates(stripped_word)
                    if corrected_word:
                        word = word.replace(stripped_word, list(corrected_word)[0])
                corrected_text.append(word)
                word = ""
            corrected_text.append(char)  # Append the whitespace character
        else:
            word += char

    # If any word is left at the end, process it
    if word:
        stripped_word = strip_punctuation(word)
        if stripped_word and spell.unknown([stripped_word]) and stripped_word.lower() not in [w.lower() for w in custom_words]:
            corrected_word = spell.candidates(stripped_word)
            if corrected_word:
                word = word.replace(stripped_word, list(corrected_word)[0])
        corrected_text.append(word)

    # Reinsert the corrected text into the text box without changing the format
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", "".join(corrected_text))
    check_spelling()  # Recheck spelling after correction
    showinfo("BirdPad", "Spellcheck complete.")

# Theme change function
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

# Apply theme
def apply_theme():
    if dark_mode:
        window.configure(bg='#2e2e2e')
        text_box.configure(bg='#333333', fg='white', insertbackground='white')
        saveas.configure(bg='#4c4c4c', fg='white')
        load.configure(bg='#4c4c4c', fg='white')
        quit_birdpad.configure(bg='#4c4c4c', fg='white')
        autocorrect_button.configure(bg='#4c4c4c', fg='white')
        theme_button.configure(bg='#4c4c4c', fg='white')  # Set dark color for the toggle button
    else:
        window.configure(bg='white')
        text_box.configure(bg='white', fg='black', insertbackground='black')
        saveas.configure(bg='orange', fg='black')
        load.configure(bg='blue', fg='white')
        quit_birdpad.configure(bg='red', fg='white')
        autocorrect_button.configure(bg='green', fg='white')
        theme_button.configure(bg='gray', fg='black')  # Set light color for the toggle button


# Tkinter setup
window = tk.Tk()
window.title('BirdPad 24.11 (Barred Brahma)')
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
    saveas = Button(window, text="Save", command=saveas_file, bg='orange', borderless=0)
    load = Button(window, text="Load", command=load_file, bg='blue', fg="white", borderless=0)
    quit_birdpad = Button(window, text="Quit", bg='red', command=quit_bpad, borderless=0)
    autocorrect_button = Button(window, text="Autocorrect", command=autocorrect, bg='green', fg="white", borderless=0)
    theme_button = Button(window, text="Toggle Theme", command=toggle_theme, borderless=0)
else:
    log("[DEBUG] Using default interface.")
    saveas = tk.Button(window, text="Save", command=saveas_file, bg='orange')
    load = tk.Button(window, text="Load", command=load_file, bg='blue', fg="white")
    quit_birdpad = tk.Button(window, text="Quit", bg='red', command=quit_bpad)
    autocorrect_button = tk.Button(window, text="Autocorrect", command=autocorrect, bg='green', fg="white")
    theme_button = tk.Button(window, text="Toggle Theme", command=toggle_theme)

saveas.pack(side=tk.LEFT, fill='both', expand=True)
load.pack(side=tk.LEFT, fill='both', expand=True)
autocorrect_button.pack(side=tk.LEFT, fill='both', expand=True)
quit_birdpad.pack(side=tk.RIGHT, fill='both', expand=True)

# Initial text
text_box.insert(tk.END, '''Thanks for installing BirdPad 24.11 Barred Brahma!''')

if len(argv) > 1 and not argv[1] == "--log" and not argv[1] == "--macos":
    load_file(argv[1])

if "--log" in argv:
    logging = True

# Default dark mode state
dark_mode = False
apply_theme()

# Button to toggle theme

#theme_button.pack(side=tk.LEFT, fill='both', expand=True)

window.mainloop()

# Log save if logging enabled
if logging:
    log_file = open("birdpad.log", "a")
    log_file.write("\n".join(logs))
    log_file.write("\n")
    log_file.close()
