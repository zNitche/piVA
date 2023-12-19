from piva.modules.module_base import ModuleBase
from piva.modules.dependencies import Dependencies
import pytesseract


class OCRModule(ModuleBase):
    @staticmethod
    def get_module_name():
        return "OCR"

    @staticmethod
    def get_dependencies():
        return [Dependencies.CAMERA_REQUIRED, Dependencies.SPEECH_SYNTHESIZER_REQUIRED]

    def process(self, *args, **kwargs):
        camera = kwargs.get("camera")
        speech_synthesizer = kwargs.get("speech_synthesizer")

        if camera and speech_synthesizer:
            image = camera.capture_image("main")

            if image:
                results = pytesseract.image_to_string(image)
                speech_synthesizer.say(results if results else "No text found")
