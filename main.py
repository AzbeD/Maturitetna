import easyocr
import cv2
from matplotlib import pyplot as plt
import logging
import tkinter
from tkinter import filedialog
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from deep_translator import GoogleTranslator

img_path = "Slike/Random/notice.png"

def izberiJezik():
    jezik = input("Vnesi jezik (en/slo): ")
    if jezik == "en":
        return 'en'
    elif jezik == "slo":
        return 'sl'
    else:
        logging.error("Napaka pri vnosu jezika")
        return None
    
def readText(jezik):
    try:
        reader = easyocr.Reader([jezik])
        img = cv2.imread(img_path)

        if img is None:
            logging.error(f"Napaka pri branju slike {img_path}")
            return None, None, None
            
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = reader.readtext(img_gray)

        if not result:
            logging.error("Ni zaznanega besedila")
            return
            
        allText =  []
        for detection in result:
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            if(detection[2] > 0.7):
                text = detection[1]
                allText.append({'text': text.lower(), 'coordinates': {'top_left': top_left, 'bottom_right': bottom_right}})
        return allText, img, result
    except Exception as e:
        logging.error(f"Napaka pri branju teksta: {e}")
        return None, None, None

def izpisTekst(allText):
    for text in allText:
        print(text['text'])
        print(text['coordinates'])
        return None
    
def prikaziSliko(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def vrniFontSize(top_left, bottom_right):
    fontscale = 1
    size = bottom_right[1] - top_left[1]
    if size > 0 and size <= 100:
        fontscale = 50
    elif size > 100 and size <= 200:
        fontscale = 60
    elif size > 200 and size <= 450:
        fontscale = 70
    elif size > 450:
        fontscale = 80
    return fontscale

def translateText(text, jezik):
    if(jezik == 'en'):
        translated_text = GoogleTranslator(source='en', target='sl').translate(text)
        return translated_text
    elif(jezik == 'sl'):
        translated_text = GoogleTranslator(source='sl', target='en').translate(text)
        return translated_text

def prekrijTekst(result, img, jezik):
    if img is None:
        logging.error("Napaka pri branju slike")
        return
    
    full_text = ""
    for detection in result:
        if(detection[2] > 0.7):
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            blurred_roi = cv2.blur(roi, (100, 100))
            img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = blurred_roi

    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for detection in result:
        if(detection[2] > 0.7):
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))

            text = detection[1]
            full_text += text + " "
            translated_text = translateText(text, jezik)
            font_size = vrniFontSize(top_left, bottom_right)
            font_path = "font/arial.ttf"
            font = ImageFont.truetype(font_path, font_size)

            draw.text((top_left[0], top_left[1]), translated_text.lower(), font=font, fill=(0, 0, 0))

    fullTranslated_text = translateText(full_text.strip(), jezik)    
    print(fullTranslated_text)
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

def Main():
    jezik = izberiJezik()
    result = readText(jezik)
    if result:
        allText, img, result1 = result
        if img is None:
            logging.error("Napaka pri branju slike")
            return
        prekrijTekst(result1, img, jezik)
        return allText
    else:
        logging.info("Brez zaznanega besedila")
        return None

if __name__ == "__main__":
    Main()