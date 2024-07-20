import tkinter as tk
import tkinter.filedialog, platform, os
from tkinter.messagebox import askyesno
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.ttk import Style
from tkinter import scrolledtext
from tkmacosx import Button
from sys import argv


logging = False

logs = []

def saveas_file():
    try:
        global fname
        fname = tk.filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("HTML files", "*.html"), ("HTM files", "*.htm"), ("Python files", "*.py"),("Arduino C++ files", "*.ino"), ("All files", "*.*")])
        logs.append(f"Save file to {fname}.")
        f = open(fname, "w")
        f.write(text_box.get("1.0", tk.END)[0:-1])
        f.close()
        print(text_box.get("1.0", tk.END)[0:-1])

        messagebox.showinfo("BirdPad", "File saved successfully")
        
    except AttributeError:
        pass

    except FileNotFoundError:
        showerror(title='BirdPad', message="File not found. (0)")

        
    except NameError:
        pass

    return fname

def save_file():
    try:
        global fname
        if fname:
            f = open(fname, 'w', encoding='utf-16')
            f.write(text_box.get("1.0", tk.END)[0:-1])
            f.close()
            
            messagebox.showinfo("BirdPad", "File saved successfully")
    except NameError:
        fname = saveas_file()

def load_file(fname=None):
    if fname:
        logs.append(f"Load file from {fname}.")
        try:
            f = open(fname, 'r')

            text_box.delete("1.0", tk.END)
            text_box.insert("1.0", f.read())

                
            f.close()

        except UnicodeDecodeError:
            showerror(title='BirdPad', message="This file is not a text document and cannot be read by BirdPad.")

        except AttributeError:
            pass

        except FileNotFoundError:
            showerror(title='BirdPad', message="File not found. (1)")
    

        except Exception as e:
            showerror(title='BirdPad', message=str(e))
    else:
        try:
            fname = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("XML files", "*.xml"), ("HTML files", "*.html"), ("HTM files", "*.htm"), ("Python files", "*.py"), ("Arduino C++ files", "*.ino"), ("All files", "*.*")])
            logs.append(f"Load file from {fname}.")
            f = open(fname, 'r')
            text_box.delete("1.0", tk.END)
            text_box.insert("1.0", f.read())
            f.close()

        except UnicodeDecodeError:
            showerror(title='BirdPad', message="This file is not a text document and cannot be read by BirdPad.")

        except AttributeError:
            pass

        except FileNotFoundError:
            if fname:
                showerror(title='BirdPad', message="File not found. (1)")
    

        except Exception as e:
            showerror(title='BirdPad', message=str(e))

def quit_bpad():
    logs.append(f"Ask if app should be closed.")
    answer = askyesno(title='Quit BirdPad', message='Are you sure that you want to quit?')
    if answer:
        window.destroy()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    logs.append(f"Get resource from {relative_path}.")
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

    
#print(os.listdir())

window = tk.Tk()

window.title('BirdPad v1.2')
window.geometry("700x700")

photo = tk.PhotoImage(file = resource_path('birdpad.png'))
window.wm_iconphoto(False, photo)

text_box = scrolledtext.ScrolledText(wrap="none", relief="sunken")
text_box.pack(expand=True, fill='both')





#save = tk.Button(window, text="Save", command=save_file)
#save.pack(side=tk.LEFT)





if platform.system() == "Darwin":
    saveas = Button(window, text="Save", command=saveas_file)
    load = Button(window, text="Load", command=load_file)
    quit_birdpad = Button(window, text="Quit", bg='red', command=quit_bpad, borderless=0)
    #birdpad_credits = Button(window, text="Credits", bg='orange', command=quit_bpad, borderless=0)

else:
    saveas = tk.Button(window, text="Save", command=saveas_file)
    load = tk.Button(window, text="Load", command=load_file)
    quit_birdpad = tk.Button(window, text="Quit", bg='red', command=quit_bpad)
    #birdpad_credits = tk.Button(window, text="Credits", bg='orange', command=quit_bpad)
    
saveas.pack(side=tk.LEFT, expand=True, fill='both')
quit_birdpad.pack(side=tk.RIGHT,  expand=True, fill='both')
#birdpad_credits.pack(side=tk.RIGHT,  expand=True, fill='both')
load.pack(side=tk.LEFT, expand=True, fill='both')


#window.resizable(False, False)

text_box.insert(tk.END, '''Thanks for installing BirdPad v1.3!

BREAKING: BirdPad is moving back to the Unlicense! See Github for more info!''')

if len(argv) > 1 and not argv[1] == "--log":
    load_file(argv[1])

if "--log" in argv:
    logging = True
    
window.mainloop()

if logging:
    log_file = open("birdpad.log", "a")
    log_file.write("\n".join(logs))
    log_file.write("\n")
    log_file.close()

