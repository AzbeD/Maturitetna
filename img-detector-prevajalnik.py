from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import easyocr
import cv2
import logging
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import matplotlib.pyplot as plt

# Initialize the main window
root = Tk()
root.title('Image Translator')
root.geometry("880x400")

# Image path (change this to a real file path or use a file picker)
img_path = "Slike/Random/barila.jpg"

def readText():
    try:
        reader = easyocr.Reader(['en'])  # Default to English OCR
        img = cv2.imread(img_path)

        if img is None:
            logging.error(f"Error reading image {img_path}")
            return None
        
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = reader.readtext(img_gray)

        if not result:
            logging.error("No text detected")
            return None
            
        extracted_text = []
        for detection in result:
            if detection[2] > 0.7:  # Confidence threshold
                extracted_text.append(detection[1])

        return " ".join(extracted_text)  # Combine detected text
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return None

def translate_it():
    translated_text.delete(1.0, END)
    try:
        from_language = original_combo.get()
        to_language = translated_combo.get()

        # Get text from OCR
        words = readText()
        if not words:
            messagebox.showerror("Error", "No text detected in the image")
            return

        # Translate text
        translation = GoogleTranslator(source=from_language, target=to_language).translate(words)
        translated_text.insert(1.0, translation)
    except Exception as e:
        messagebox.showerror("Translator", str(e))

def clear():
    translated_text.delete(1.0, END)

# Language list for combobox
language_list = ["auto"] + GoogleTranslator().get_supported_languages()

# Buttons and Text Boxes
translate_button = Button(root, text="Translate Image", font=("Helvetica", 18), command=translate_it)
translate_button.pack(pady=10)

translated_text = Text(root, height=10, width=60)
translated_text.pack(pady=10)

# Language selection
original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current(language_list.index("auto"))
original_combo.pack()

translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(language_list.index("english"))
translated_combo.pack()

clear_button = Button(root, text="Clear", command=clear)
clear_button.pack(pady=5)

root.mainloop()
