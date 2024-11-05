# old code ripped out from production - do not use

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

