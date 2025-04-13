import logging
import numpy as np
import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from main import Main

class OCRApp(App):
    def build(self):
        self.img_path = "captured_image.jpg"
        self.language = None

        layout = BoxLayout(orientation='vertical')

        self.camera = Camera(play=True, resolution=(640, 480))
        layout.add_widget(self.camera)

        self.language_input = TextInput(hint_text="Enter language (en/slo)", multiline=False)
        layout.add_widget(self.language_input)

        capture_button = Button(text="Capture Image")
        capture_button.bind(on_press=self.capture_image)
        layout.add_widget(capture_button)

        process_button = Button(text="Process Image")
        process_button.bind(on_press=self.process_image)
        layout.add_widget(process_button)

        self.image_widget = Image()
        layout.add_widget(self.image_widget)

        return layout

    def capture_image(self, instance):
        captured_image = self.camera.texture
        if captured_image:
            buf = captured_image.pixels
            img = np.frombuffer(buf, dtype=np.uint8).reshape(captured_image.height, captured_image.width, 4)
            cv2.imwrite(self.img_path, cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
            logging.info(f"Image captured and saved to {self.img_path}")

    def process_image(self, instance):
        self.language = self.language_input.text.strip()

        if not self.language:
            logging.error("Please enter a language.")
            return

        processed_img = Main(self.img_path, self.language)
        if processed_img is not None:
            self.display_image(processed_img)

    def display_image(self, img):
        buf = cv2.flip(img, 0).tobytes()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture
    
if __name__ == "__main__":
    OCRApp().run()