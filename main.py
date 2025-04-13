import easyocr
import cv2
import logging
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from deep_translator import GoogleTranslator

def readText(jezik, img_path):
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
            height = bottom_right[1] - top_left[1]
            if(detection[2] > 0.7) and (height > 150):  
                text = detection[1]
                allText.append({'text': text.lower(), 'coordinates': {'top_left': top_left, 'bottom_right': bottom_right}})
        return allText, img, result
    except Exception as e:
        logging.error(f"Napaka pri branju teksta: {e}")
        return None, None, None
 

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

def translateText(text, izvorniJezik, ciljniJezik):
    try:
        translated_text = GoogleTranslator(source=izvorniJezik, target=ciljniJezik).translate(text)
        return translated_text
    except Exception as e:
        logging.error(f"Napaka pri prevajanju: {e}")
        return text


def prekrijTekst(result, img, izvorniJezik, ciljniJezik):
    if img is None:
        logging.error("Napaka pri branju slike")
        return
      
    full_text = ""
    for detection in result:
        top_left = tuple(map(int, detection[0][0]))
        bottom_right = tuple(map(int, detection[0][2]))
        height = bottom_right[1] - top_left[1]
        if(detection[2] > 0.7) and (height > 0):
            roi = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
            blurred_roi = cv2.blur(roi, (100, 100))
            img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = blurred_roi

    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for detection in result:
        top_left = tuple(map(int, detection[0][0]))
        bottom_right = tuple(map(int, detection[0][2]))
        height = bottom_right[1] - top_left[1]
        if(detection[2] > 0.7) and (height > 0):
            text = detection[1]
            full_text += text + " "
            translated_text = translateText(text, izvorniJezik, ciljniJezik)
            font_size = vrniFontSize(top_left, bottom_right)
            font_path = "font/arial.ttf"
            font = ImageFont.truetype(font_path, font_size)
            draw.text((top_left[0], top_left[1]), translated_text.lower(), font=font, fill=(0, 0, 0))

    fullTranslated_text = translateText(full_text.strip(), izvorniJezik, ciljniJezik)    
    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    return img

def Main(img_path, izvorniJezik, ciljniJezik):
    result = readText(izvorniJezik, img_path)
    if result:
        allText, img, result1 = result
        if img is None:
            logging.error("Napaka pri branju slike")
            return
        img = prekrijTekst(result1, img, izvorniJezik, ciljniJezik)
        return img
    else:
        logging.info("Brez zaznanega besedila")
        return None

if __name__ == "__main__":
    Main("Slike/Random/dnevnik.jpg", "sl")