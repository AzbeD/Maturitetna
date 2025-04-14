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
from kivy.uix.spinner import Spinner
from main import Main

class OCRApp(App):
    def build(self):
        self.img_path = "captured_image.jpg"
        self.language = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.camera = Camera(play=True, resolution=(1280, 720))  # Increased resolution for better quality
        layout.add_widget(self.camera)

        # Language input
        self.language_from_spinner = Spinner(
            text="Izberi izvorni jezik",
            values=[
                'angleščina', 'francoščina', 'grščina', 'hrvaščina', 'italijanščina', 'nemščina',
                'poljščina', 'portugalščina', 'romunščina', 'ruščina', 'srbščina', 'slovaščina',
                'slovenščina', 'španščina'
            ],
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.language_from_spinner)        


        self.language_to_spinner = Spinner(
            text="Izberi ciljni jezik",
            values=[
                'angleščina', 'francoščina', 'grščina', 'hrvaščina', 'italijanščina', 'nemščina',
                'poljščina', 'portugalščina', 'romunščina', 'ruščina', 'srbščina', 'slovaščina',
                'slovenščina', 'španščina'
            ],
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.language_to_spinner)

        capture_process_button = Button(text="Zajemi in sprocesiraj sliko", size_hint_y=None, height=50)
        capture_process_button.bind(on_press=self.capture_and_process)
        layout.add_widget(capture_process_button)

        self.image_widget = Image(size_hint_y=None, height=400)
        layout.add_widget(self.image_widget)

        return layout

    def capture_and_process(self, instance):
        captured_image = self.camera.texture
        if captured_image:
            buf = captured_image.pixels
            img = np.frombuffer(buf, dtype=np.uint8).reshape(captured_image.height, captured_image.width, 4)
            cv2.imwrite(self.img_path, cv2.cvtColor(img, cv2.COLOR_RGBA2BGR))
            logging.info(f"Slika zajeta in shranjena v {self.img_path}")

        selected_language_from = self.language_from_spinner.text
        selected_language_to = self.language_to_spinner.text
        language_map = {
            'angleščina': 'en', 'francoščina': 'fr', 'grščina': 'el', 'hrvaščina': 'hr',
            'italijanščina': 'it', 'nemščina': 'de', 'poljščina': 'pl', 'portugalščina': 'pt',
            'romunščina': 'ro', 'ruščina': 'ru', 'srbščina': 'sr', 'slovaščina': 'sk',
            'slovenščina': 'sl', 'španščina': 'es'
        }
        self.language_from = language_map.get(selected_language_from)
        self.language_to = language_map.get(selected_language_to)
        print(f"Selected languages: {self.language_from} to {self.language_to}")
        if not self.language_to or not self.language_from:
            logging.error("Prosimo izberite oba izvorni in ciljni jezik.")
            return

        processed_img = Main(self.img_path, self.language_from, self.language_to)
        if processed_img is not None:
            self.display_image(processed_img)

    def display_image(self, img):
        buf = cv2.flip(img, 0).tobytes()
        texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image_widget.texture = texture

if __name__ == "__main__":
    OCRApp().run()