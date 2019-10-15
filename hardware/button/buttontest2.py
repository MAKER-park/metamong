import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True :
	button_input_1 = GPIO.input(3)
	button_input_2 = GPIO.input(5)
	button_input_3 = GPIO.input(7)
	button_input_4 = GPIO.input(8)	
	if button_input_1 == False:
		print("Button1 red Pressed")
		time.sleep(0.3)
	if button_input_2 == False:
                print("Button2 yellow Pressed")
                time.sleep(0.3)
	if button_input_3 == False:
                print("Button3 green Pressed")
                time.sleep(0.3)
	if button_input_4 == False:
                print("Button4 blue Pressed")
                time.sleep(0.3)


GPIO.cleanup()
