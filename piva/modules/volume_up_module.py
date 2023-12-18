from piva.modules.module_base import ModuleBase
from piva.modules.dependencies import Dependencies


class VolumeUpModule(ModuleBase):
    @staticmethod
    def get_module_name():
        return "VolumeUp"

    @staticmethod
    def get_dependencies():
        return [Dependencies.AUDIO_MIXER_REQUIRED, Dependencies.SPEECH_SYNTHESIZER_REQUIRED]

    def process(self, *args, **kwargs):
        audio_mixer = kwargs.get("audio_mixer")
        speech_synthesizer = kwargs.get("speech_synthesizer")

        if audio_mixer:
            current_volume = audio_mixer.getvolume()
            volume = current_volume + 10 if current_volume + 10 < 100 else 100

            audio_mixer.setvolume(volume)

            if speech_synthesizer:
                speech_synthesizer.say(f"Current volume level {audio_mixer.getvolume()}")
