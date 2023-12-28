import button_logic as bl
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

bl.init_buttons()

while True:
	bl.poll_button()