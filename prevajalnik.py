from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

root = Tk()
root.title('Translator')
root.geometry("880x300")

def translate_it():
    translated_text.delete(1.0, END)
    try:
        from_language_key = original_combo.get()
        to_language_key = translated_combo.get()
        words = original_text.get(1.0, END).strip()

        translation = GoogleTranslator(source=from_language_key, target=to_language_key).translate(words)
        translated_text.insert(1.0, translation)
    except Exception as e:
        messagebox.showerror("Translator", str(e))

def clear():
    original_text.delete(1.0, END)
    translated_text.delete(1.0, END)

language_list = ["auto"] + GoogleTranslator().get_supported_languages()


original_text = Text(root, height=10, width=40)
original_text.grid(row=0, column=0, pady=20, padx=10)

translate_button = Button(root, text="Translate!", font=("Helvetica", 24), command=translate_it)
translate_button.grid(row=0, column=1, padx=10)

translated_text = Text(root, height=10, width=40)
translated_text.grid(row=0, column=2, pady=20, padx=10)

original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current(language_list.index("auto"))
original_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(language_list.index("english"))  
translated_combo.grid(row=1, column=2)

clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=2, column=1)

root.mainloop()