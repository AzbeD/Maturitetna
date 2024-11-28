import easyocr
import cv2
from matplotlib import pyplot as plt

img_path = "Slike/ucbenik.jpg"

def readText():
    jezik = izberiJezik()
    if jezik:
        reader = easyocr.Reader([jezik])
        img = cv2.imread(img_path)

        if img is None:
            print(f"Error: Unable to load image at {img_path}")
            return
        
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = reader.readtext(img_gray)

        if not result:
            print("No text detected in the image.")
            return
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        allText =  []
        for detection in result:
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            text = detection[1]
            img = cv2.rectangle(img, top_left, bottom_right, (0,255,0), 3)
            allText.append({'text': text.lower(), 'coordinates': {'top_left': top_left, 'bottom_right': bottom_right}})
        return allText, img
    else:
        print("Napaka pri vnosu jezika")

def izberiJezik():
    jezik = input("Vnesi jezik (en/slo): ")
    if jezik == "en":
        return 'en'
    elif jezik == "slo":
        return 'sl'
    else:
        print("Napaka pri vnosu jezika")
        return None
    
def getCoords(allText):
    for text in allText:
        print(text['text'])
        print(text['coordinates'])

def Main():
    result = readText()
    if result:
        allText, img = result
        getCoords(allText)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        print("Napaka pri branju besedila")

if __name__ == "__main__":
    Main()
