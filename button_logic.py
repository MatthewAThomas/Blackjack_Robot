import time
import RPi.GPIO as GPIO

# SOME OF THE LOWER GPIO PINS ARE PULLED UP BY DEFAULT (use a higher pin)
hitButton = 6
standButton = 5

def init_buttons():
	GPIO.setup(hitButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(standButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



""" Returns true if hit, false if stand """
def poll_button():
	# while GPIO.input(hitButton) == 0 and GPIO.input(standButton):
	#    time.sleep(1)
	hit = 0
	stand = 0
			
	while True:
		hit = GPIO.input(hitButton)
		stand = GPIO.input(standButton)
		if hit:
			print("Hit!")
			time.sleep(1)
			hit = 0
			stand = 0
			return True

		if stand:
			print("Stand!")
			hit = 0
			stand = 0
			
			time.sleep(1)
			return False