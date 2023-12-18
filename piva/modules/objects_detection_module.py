from piva.modules.module_base import ModuleBase
from piva.modules.dependencies import Dependencies
from piva.detector import detect


class ObjectsDetectionModule(ModuleBase):
    @staticmethod
    def get_module_name():
        return "ObjectsDetection"

    @staticmethod
    def get_dependencies():
        return [Dependencies.CAMERA_REQUIRED, Dependencies.SPEECH_SYNTHESIZER_REQUIRED]

    def process(self, *args, **kwargs):
        camera = kwargs.get("camera")
        speech_synthesizer = kwargs.get("speech_synthesizer")

        if camera and speech_synthesizer:
            image = camera.capture_image("main")

            if image:
                results = detect.process(image)
                classes_count = self.__count_classed(results)

                speech_synthesizer.say(self.__generate_text_for_results(classes_count))

    def __generate_text_for_results(self, classes):
        text = ""

        for cl in classes:
            text += f"{classes[cl]} {cl}, "

        return "no objects has been found" if len(classes.keys()) == 0 else text

    def __count_classed(self, results):
        counted_classed = {}

        for cl in results:
            if cl["class"] not in counted_classed.keys():
                counted_classed[cl["class"]] = 0

            counted_classed[cl["class"]] += 1

        return counted_classed
