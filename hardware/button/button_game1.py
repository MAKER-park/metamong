#mini game + button =================================

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from random import randint

Qlen = 6  #문제 출제길이 6번 깜빡임
quiz = [0]*6  #랜드인트 6개저장, 답 확인시 사용
answer = [0]*6 #사용자 정답 저장
count=0
userinput=0

i=0
print("< Quiz > ")
for i in range(Qlen):
    quiz.append(randint(1,4))  #버튼인덱스 리스트에 저장, 답 확인시 사용
    quiz[i]=randint(1,4)
    print(quiz[i], end = " ")  #버튼의 불빛을 순서대로 보여줌 /  불빛은 인덱스 지정해놔야
print("\n\n")

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(False)                  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)            # Use physical pin numbering
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #1
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #2
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #3
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)        #4

while True:
        if (GPIO.input(3) == False):   #빨강
                print("Button1 Pressed")
               # answer.append(1)
                userinput = 1
                time.sleep(0.5)
                count+=1

        if (GPIO.input(5) == False):   #노랑
                print("Button2 Pressed")
               # answer.append(2)
                userinput = 2
                time.sleep(0.5)
                count+=1

        if (GPIO.input(7) == False):   #초록
                print("Button3 Pressed")
               # answer.append(3)
                userinput = 3
                time.sleep(0.5)
                count+=1

        if (GPIO.input(8) == False):   #파랑
                print("Button4 Pressed")
                #print(count)
               # answer.append(4)
                userinput = 4
                time.sleep(0.5)
                count+=1

        answer[count-1]=userinput

        if (count == 6):
                break

#유저 인풋값 확인용 프린트- 확인 후 지워도 괜찮음
print(answer)
#---------------------------------------------------------

b = 0
cnt = 0
for b in range(Qlen):
    if(quiz[b] != answer[b]):  #순서 비교
        print("틀렸습니다")
        break
    else:
        cnt +=1
        print("Answer : ", quiz[cnt])
if(cnt == 6):
    print("모두 맞았습니다")

GPIO.cleanup()

