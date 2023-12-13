import RPi.GPIO as GPIO
import time


def init_shoot():
    global CHANNEL_1
    global CHANNEL_2
    global pwm1
    global pwm2

    # GPIO.setmode(GPIO.BCM)

    CHANNEL_1 = 17
    CHANNEL_2 = 18

    #Set up GPIO
    GPIO.setup(CHANNEL_1, GPIO.OUT)
    GPIO.setup(CHANNEL_2, GPIO.OUT)
    pwm1 = GPIO.PWM(CHANNEL_1, 5000)
    pwm2 = GPIO.PWM(CHANNEL_2, 5000)

def drive_forward():
    GPIO.output(CHANNEL_1, GPIO.HIGH)
    GPIO.output(CHANNEL_2, GPIO.LOW)
   # pwm1.start(80)

def drive_backward():
    GPIO.output(CHANNEL_1, GPIO.LOW)
    GPIO.output(CHANNEL_2, GPIO.HIGH)
    #pwm2.start(80)

def stop_motor():
    GPIO.output(CHANNEL_1, GPIO.LOW)
    GPIO.output(CHANNEL_2, GPIO.LOW)

def shoot():
    drive_forward()
    time.sleep(0.220)
    stop_motor()
    pwm1.stop()

    drive_backward()
    time.sleep(0.5)
    stop_motor()
    pwm2.stop()
