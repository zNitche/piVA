import RPi.GPIO as GPIO
from picamera2 import Picamera2
import alsaaudio
from piva.config import Config
from piva.helpers.speech_synthesizer import SpeechSynthesizer
from piva.helpers.task_thread import TaskThread
from piva.modules.dependencies import Dependencies as ModulesDependencies


class PiVA:
    def __init__(self, debug=False):
        self.task_handler = TaskThread()

        self.camera = None
        self.audio_mixer = None
        self.speech_synthesizer = None

        self.modules = []
        self.current_mode = None

        self.initialized = False

        self.debug = debug

    def start(self):
        if not self.initialized:
            self.__log("PiVA setup started...")

            self.__init_audio()
            self.__init_camera()
            self.__setup_buttons()
            self.__setup_modules()

            self.initialized = True
            self.__log("PiVA setup completed...")

    def __init_audio(self):
        self.__log("Audio init...")

        self.audio_mixer = alsaaudio.Mixer("PCM")
        self.speech_synthesizer = SpeechSynthesizer()

        self.__log("Audio ready...")

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
        GPIO.add_event_detect(Config.ACCEPT_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback,
                              bouncetime=2000)

        GPIO.setup(Config.UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(Config.UP_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback,
                              bouncetime=2000)

        GPIO.setup(Config.DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(Config.DOWN_BUTTON_PIN, GPIO.RISING, callback=self.__button_pressed_callback,
                              bouncetime=2000)

        self.__log("Buttons ready...")

    def __setup_modules(self):
        self.__log("Modules init...")

        from piva.modules.objects_detection_module import ObjectsDetectionModule
        from piva.modules.volume_up_module import VolumeUpModule
        from piva.modules.volume_down_module import VolumeDownModule
        from piva.modules.ocr_module import OCRModule

        self.modules = [ObjectsDetectionModule(), OCRModule(), VolumeUpModule(), VolumeDownModule()]
        self.current_mode = self.modules[0]

        self.__log("Modules ready...")

    def __button_pressed_callback(self, channel):
        if self.initialized:
            self.__log(f"button {channel} pressed")
            self.__handle_button(channel)

    def __handle_button(self, button_id):
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
            if not self.task_handler.is_running:
                self.__log(f"Executing {self.current_mode.get_module_name()}...")
                self.speech_synthesizer.say(f"Executing {self.current_mode.get_module_name()}")

                func = lambda: self.current_mode.process(**self.__resolve_module_dependencies(self.current_mode))
                self.task_handler.run(func)
            else:
                self.__log(f"Currently processing...")
                self.speech_synthesizer.say("Currently processing")

    def __resolve_module_dependencies(self, module):
        dependencies = {
            "camera": self.__get_dependency(ModulesDependencies.CAMERA_REQUIRED, module, self.camera),
            "audio_mixer": self.__get_dependency(ModulesDependencies.AUDIO_MIXER_REQUIRED, module, self.audio_mixer),
            "speech_synthesizer": self.__get_dependency(ModulesDependencies.SPEECH_SYNTHESIZER_REQUIRED, module, self.speech_synthesizer)
        }

        return dependencies

    def __get_dependency(self, dependency, module, return_value):
        return return_value if dependency in module.get_dependencies() else None

    def __switch_to_prev_module(self):
        current_module_id = self.modules.index(self.current_mode)

        self.current_mode = self.modules[len(self.modules) - 1] if current_module_id - 1 < 0 \
            else self.modules[current_module_id - 1]

        self.speech_synthesizer.say(f"Current mode {self.current_mode.get_module_name()}")

    def __switch_to_next_module(self):
        current_module_id = self.modules.index(self.current_mode)

        self.current_mode = self.modules[0] if current_module_id + 1 >= len(self.modules) \
            else self.modules[current_module_id + 1]

        self.speech_synthesizer.say(f"Current mode {self.current_mode.get_module_name()}")

    def __log(self, message):
        if self.debug:
            print(message)
