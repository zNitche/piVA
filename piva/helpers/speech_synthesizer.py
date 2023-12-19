import subprocess


class SpeechSynthesizer:
    def __init__(self):
        pass

    def say(self, text):
        return subprocess.run(["espeak", text])
