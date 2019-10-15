
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from random import randint

oddEven = randint(0,1) #홀짝
userInput =0
count = 0
print("홀 짝 게임입니다. 1번과 2번 버튼중 아무 버튼을 눌러 주세요.!")
#print(oddEven) # 정답출력용 / 유저한테는 안보이게

def button_callback(channel):
	print("Button was pushed!")
GPIO.setwarnings(False)                  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)            # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #1
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #2
#GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #3
#GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #4

while True:

	button_1 = GPIO.input(3)
	button_2 = GPIO.input(5)

	if (button_1 == False):     #1번 버튼: 홀수
		print("Button1 Pressed")
		count = 1
		userInput = 1
		time.sleep(0.3)
		if(oddEven == userInput):
			print("정답이다!")
			break
		elif(oddEven != userInput):
			print("오답이다!")
			break

	elif (button_2 == False):   #2번 버튼: 짝수
		print("Button2 Pressed")
		count = 1
		userInput = 0
		time.sleep(0.3)
		if(oddEven == userInput):
			print("정답이다!")
			break
		elif(oddEven != userInput):
			print("오답이다!")
			break

		#if(count == 1):
		#break

			#if(oddEven == userInput):
			#	print("Answer!")
			#	break

			#elif(oddEven != userInput):
			#	print("Wrong!")
			#	break

GPIO.cleanup()



