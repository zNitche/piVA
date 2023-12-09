from piva.modules.module_base import ModuleBase
from piva.modules.dependencies import Dependencies
from piva.detector import detect


class ObjectsDetectionModule(ModuleBase):
    @staticmethod
    def get_module_name():
        return "ObjectsDetection"

    @staticmethod
    def get_dependencies():
        return [Dependencies.CAMERA_REQUIRED]

    def process(self, *args, **kwargs):
        camera = kwargs["camera"]

        if camera:
            image = camera.capture_image("main")

            if image:
                results = detect.process(image)

                print(results)
