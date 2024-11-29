import easyocr
import cv2
from matplotlib import pyplot as plt
import logging
import tkinter
from tkinter import filedialog

img_path = "Slike/knjiga.jpg"
#tkinter.Tk().withdraw()
#img_path = filedialog.askopenfilename()

def readText(jezik):
    try:
        reader = easyocr.Reader([jezik])
        img = cv2.imread(img_path)

        if img is None:
            logging.error(f"Napaka pri branju slike {img_path}")
            return
            
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = reader.readtext(img_gray)

        if not result:
            logging.error("Ni zaznanega besedila")
            return
            
        allText =  []
        for detection in result:
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            text = detection[1]
            img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 3)
            allText.append({'text': text.lower(), 'coordinates': {'top_left': top_left, 'bottom_right': bottom_right}})
        return allText, img
    except Exception as e:
        logging.error(f"Napaka pri branju teksta: {e}")
        return None

def izberiJezik():
    jezik = input("Vnesi jezik (en/slo): ")
    if jezik == "en":
        return 'en'
    elif jezik == "slo":
        return 'sl'
    else:
        logging.error("Napaka pri vnosu jezika")
        return None
    
def izpisTekst(allText):
    for text in allText:
        print(text['text'])
        print(text['coordinates'])

def Main():
    jezik = izberiJezik()
    result = readText(jezik)
    if result:
        allText, img = result
        izpisTekst(allText)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        logging.info("Brez zaznanega besedila")

if __name__ == "__main__":
    Main()
