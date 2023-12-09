import RPi.GPIO as GPIO
import signal
import sys
from piva.piva import PiVA


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def main():
    piva = PiVA(debug=True)
    piva.start()


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    main()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
