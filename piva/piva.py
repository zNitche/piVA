import RPi.GPIO as GPIO
from picamera2 import Picamera2
from piva.config import Config
from piva.modules.dependencies import Dependencies as ModulesDependencies


class PiVA:
    def __init__(self, debug=False):
        self.camera = None
        self.modules = []
        self.current_mode = None

        self.initialized = False
        self.processing = False

        self.debug = debug

    def start(self):
        if not self.initialized:
            self.__log("PiVA setup started...")

            self.__init_camera()
            self.__setup_buttons()
            self.__setup_modules()

            self.initialized = True
            self.__log("PiVA setup completed...")

    def __init_camera(self):
        self.__log("Camera init...")

        cam = Picamera2()
        config = cam.create_still_configuration(main={"size": (Config.CAMERA_WIDTH, Config.CAMERA_HEIGHT)})
        cam.configure(config)

        cam.start()
        self.camera = cam

        self.__log("Camera ready...")

    def __setup_buttons(self):
        self.__log("Buttons init...")
        GPIO.setup(Config.ACCEPT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(Config.ACCEPT_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback, bouncetime=1000)

        GPIO.setup(Config.UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(Config.UP_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback, bouncetime=1000)

        GPIO.setup(Config.DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(Config.DOWN_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback, bouncetime=1000)

        self.__log("Buttons ready...")

    def __setup_modules(self):
        self.__log("Modules init...")

        from piva.modules.objects_detection_module import ObjectsDetectionModule

        self.modules = [ObjectsDetectionModule()]
        self.current_mode = self.modules[0]

        self.__log("Modules ready...")

    def __button_pressed_callback(self, channel):
        if self.initialized:
            self.__log(f"button {channel} pressed")
            self.__handle_button(channel)

    def __handle_button(self, button_id):
        if not self.processing:
            if button_id == Config.ACCEPT_BUTTON_PIN:
                self.__execute_current_module()

            elif button_id == Config.UP_BUTTON_PIN:
                self.__switch_to_next_module()

            elif button_id == Config.DOWN_BUTTON_PIN:
                self.__switch_to_prev_module()

            else:
                self.__log(f"unsupported button id: {button_id}")

    def __execute_current_module(self):
        if self.current_mode:
            self.__log(f"Executing {self.current_mode.get_module_name()}...")

            self.processing = True

            args = {
                "camera": self.camera if ModulesDependencies.CAMERA_REQUIRED in self.current_mode.get_dependencies() else None
            }

            self.current_mode.process(**args)
            self.processing = False

    def __switch_to_prev_module(self):
        pass

    def __switch_to_next_module(self):
        pass

    def __log(self, message):
        if self.debug:
            print(message)
