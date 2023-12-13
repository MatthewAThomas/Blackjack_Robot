import RPi.GPIO as GPIO
import time

DIR = 22
STEP = 23
steps_per_rev = 200

GPIO.setmode(GPIO.BCM)

def init_rotate():
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

def spin_clockwise(steps):
    print("Spinning Clockwise...")
    GPIO.output(DIR, GPIO.HIGH)

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(0.001)
        #time.sleep(0.003)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(0.001)
        #time.sleep(0.003)

    time.sleep(1)

def spin_anticlockwise(steps):
    print("Spinning Anti-Clockwise...")
    GPIO.output(DIR, GPIO.LOW)

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(0.001)
        #time.sleep(0.003)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(0.001)
        #time.sleep(0.003)

    time.sleep(1)
