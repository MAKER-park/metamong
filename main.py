from tkinter import *
import tkinter.font
from random import *
import pandas as pd
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import threading
from multiprocessing.pool import ThreadPool
import time

max_point = 40
p_capital = 0
p_technology = 0
p_passion = 0
p_fame = 0

global job, ms
job = pd.read_csv("jobCard.csv")
ms = pd.read_csv("missionCard.csv", encoding='utf-8')

global crrt_job

global dice_num
dice_num = ""

drink = ["데자와", "솔의눈", "민트초코", "핫식스", "아아메", "박카스"]  # 랜덤하게
toplevel = Tk()
font = tkinter.font.Font(family="나눔스퀘어", size=18)
font_big = tkinter.font.Font(family="나눔스퀘어", size=24)

def minigame2():
    oddEven = randint(0, 1)  # 홀짝
    userInput = 0
    count = 0
    print(oddEven)  # 정답출력용 / 유저한테는 안보이게

    def dst(r):
        r.destroy()
        rolling_dice()

    def button_callback(channel):
        print("Button was pushed!")

    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 1
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 2

    #버튼을 눌러주세요
    pop = Toplevel(toplevel)
    pop.geometry("1024x600+0+0")
    pop.title("미니게임!")
    pop.resizable(False, False)
    pop.configure(background="white")

    text = tkinter.Label(pop, text="\n\n\n\n미니게임!\n\n"
                         "홀수 또는 짝수 번호를 눌러주세요.",
                        font=font, background="white")
    text.pack()
    toplevel.mainloop()

    while True:
        button_1 = GPIO.input(3)
        button_2 = GPIO.input(5)

        if (button_1 == False):  # 1번 버튼: 홀수
            print("Button1 Pressed")
            count = 1
            userInput = 1
            if (oddEven == userInput):
                print("정답이다!")
                pop1 = Toplevel(toplevel)
                pop1.geometry("1024x600+0+0")
                pop1.title("미니게임!")
                pop1.resizable(False, False)
                pop1.configure(background="white")
                text4 = tkinter.Label(pop1, text="정답입니다! 점수 획득!",
                                     font=font, background="white")
                text4.pack()
                btn22 = Button(pop1, command=lambda: dstd(pop1), background="#c8e6ee")
                btn22.config(text='다음으로 진행', font=font)
                btn22.pack()
                btn22.place(x=330, y=480)
                toplevel.mainloop()
                return
            elif (oddEven != userInput):
                print("오답이다!")
                pop1 = Toplevel(toplevel)
                pop1.geometry("1024x600+0+0")
                pop1.title("미니게임!")
                pop1.resizable(False, False)
                pop1.configure(background="white")
                text4 = tkinter.Label(pop1, text="정답입니다! 점수 획득!",
                                     font=font, background="white")
                text4.pack()
                btn22 = Button(pop1, command=lambda: dstd(pop1), background="#c8e6ee")
                btn22.config(text='다음으로 진행', font=font)
                btn22.pack()
                btn22.place(x=330, y=480)
                toplevel.mainloop()
                return

        elif (button_2 == False):  # 2번 버튼: 짝수
            print("Button2 Pressed")
            count = 1
            userInput = 0
            if (oddEven == userInput):
                print("정답이다!")
                pop1 = Toplevel(toplevel)
                pop1.geometry("1024x600+0+0")
                pop1.title("미니게임!")
                pop1.resizable(False, False)
                pop1.configure(background="white")
                text4 = tkinter.Label(pop1, text="정답입니다! 점수 획득!",
                                     font=font, background="white")
                text4.pack()
                btn22 = Button(pop1, command=lambda: dstd(pop1), background="#c8e6ee")
                btn22.config(text='다음으로 진행', font=font)
                btn22.pack()
                btn22.place(x=330, y=480)
                toplevel.mainloop()
                return
            elif (oddEven != userInput):
                print("오답이다!")
                pop1 = Toplevel(toplevel)
                pop1.geometry("1024x600+0+0")
                pop1.title("미니게임!")
                pop1.resizable(False, False)
                pop1.configure(background="white")
                text4 = tkinter.Label(pop1, text="정답입니다! 점수 획득!",
                                     font=font, background="white")
                text4.pack()
                btn22 = Button(pop1, command=lambda: dstd(pop1), background="#c8e6ee")
                btn22.config(text='다음으로 진행', font=font)
                btn22.pack()
                btn22.place(x=330, y=480)
                toplevel.mainloop()
                return

    GPIO.cleanup()
    #toplevel.mainloop()


# 주사위 굴릴 때, 음료수 정해 줄 때 호출하는 랜덤함수 (음료수도 6개, 주사위 눈도 6까지)
def rand_six(panel):
    global dice_num
    dice_num = randint(1, 6)
    tt = dice_num, "칸 만큼 이동해주세요."
    text = tkinter.Label(panel, text=tt, font=font_big, background="white")
    text.pack()


def end_game():
    if p_capital >= max_point:
        return True
    elif p_fame >= max_point:
        return True
    elif p_passion >= max_point:
        return True
    elif p_technology >= max_point:
        return True
    else:
        return False


def card():
    def dstd(r):
        r.destroy()
        minigame2()

    pop = Toplevel(toplevel)
    pop.geometry("1024x600+0+0")
    pop.title("미션 카드 오픈")
    pop.resizable(False, False)
    pop.configure(background="white")

    def defi():
        text = tkinter.Label(pop, text="\n\n\n\n해당 위치의 미션 카드를 리더기 위에\n"
                                       "올려 주세요\n\n",
                             font=font, background="white")
        text.pack()

        temp_id = None
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(rfid)

        temp_id = async_result.get()
        print(temp_id)

        if (temp_id != None):
            text.destroy()
            text2 = tkinter.Label(pop, text="\n\n미션 공개!\n\n",
                                  font=font, background="white")
            text2.pack()
            iiii = randint(0, 16)
            t1 = ms.ix[iiii]['story']
            t2 = ms.ix[iiii]['main']
            t3 = ms.ix[iiii]['sub']

            text21 = tkinter.Label(pop, text=t1,
                                   font=font, background="white")
            text21.pack()
            text22 = tkinter.Label(pop, text=t2,
                                   font=font, background="white")
            text22.pack()
            text23 = tkinter.Label(pop, text=t3,
                                   font=font, background="white")
            text23.pack()

            btn22 = Button(pop, command=lambda: dstd(pop), background="#c8e6ee")
            btn22.config(text='다음으로 진행', font=font)
            btn22.pack()
            btn22.place(x=330, y=480)

        toplevel.mainloop()

    t = threading.Thread(target=defi)
    t.start()


def rolling_dice():
    def dstd(r):
        r.destroy()
        card()

    dice_pop = Toplevel(toplevel)
    dice_pop.geometry("1024x600+0+0")
    dice_pop.title("굴려굴려 주사위~~")
    dice_pop.resizable(False, False)
    dice_pop.configure(background="white")

    diceImg = PhotoImage(file="dice.png")
    rd = Button(dice_pop, command=lambda: rand_six(dice_pop), background="white", relief='flat')
    rd.config(image=diceImg)
    rd.pack()
    rd.place(x=360, y=130)

    btn22 = Button(dice_pop, command=lambda: dstd(dice_pop), background="#c8e6ee")
    btn22.config(text='다음으로 진행', font=font)
    btn22.pack()
    btn22.place(x=330, y=480)

    toplevel.mainloop()


def tutorial():
    def dstr(event):
        print("dd")
        ttl.destroy()

    ttl = Toplevel(toplevel)
    ttl.geometry("1024x600+0+0")
    ttl.title("설명 및 튜토리얼")
    ttl.resizable(False, False)
    ttl.configure(background="white")

    frame = Frame(ttl, width=1024, height=600)
    text = tkinter.Label(frame, text="\n\n\n\n관교를 발전시켜 게임에 성공하는 방법은 간단합니다.\n"
                                     "모두가 협력하여 주어진 미션을 수행하고, '성공점수'를 모으는 것입니다.\n\n"
                                     "각각의 유저는 기본점수로 체력, 스트레스 점수 40점을 가지고 시작합니다.\n\n",
                         font=font, background="white")
    text.pack()

    frame.pack()
    ttl.bind("<Button-1>", dstr)


def opening():
    btn1.destroy()
    text = tkinter.Label(toplevel, text="\n\n\n\n안녕하세요, 지금부터 <관교폴리> 게임을 시작하겠습니다.\n\n"
                                        "여러분은 대한민국의 새로운 계획도시 - '관교'를 \n세계 최고의 IT 집적 단지로 성장시키기 위한 인재들입니다.\n\n"
                                        "지금부터 협력 게임 진행을 통해 관교를 멋지게 발전 시켜 주세요.\n\n"
                                        "게임 설명과 방법이 궁금하시다면 <튜토리얼 보기> 버튼을 눌러주세요", font=font, background="white")
    text.pack()
    btn2 = Button(toplevel, command=tutorial, background="#c8e6ee")
    btn2.config(text='튜토리얼 보기', font=font)
    btn2.pack()
    btn2.place(x=300, y=380)

    btn3 = Button(toplevel, command=read_job_card, background="#c8e6ee")
    btn3.config(text='튜토리얼 필요 없어요!', font=font)
    btn3.pack()
    btn3.place(x=500, y=380)


global t_flag
t_flag = 0


# 직업카드 RFID 리딩하기
def read_job_card():
    rjc = Toplevel(toplevel)
    rjc.geometry("1024x600+0+0")
    rjc.title("설명 및 튜토리얼")
    rjc.resizable(False, False)
    rjc.configure(background="white")

    def defi():
        text = tkinter.Label(rjc, text="\n\n\n\n열두장의 직업카드 내용을 보지 않고 잘 섞으신 후,\n"
                                       "각자 한 장씩 카드를 뽑아 리더기에 각자의 직업을 등록 해 주세요.", font=font, background="white")
        text.pack()
        temp = [0, 0, 0, 0]
        time.sleep(5)

        for k in range(len(temp)):
            rjc2 = Toplevel(rjc)
            rjc2.geometry("1024x600+0+0")
            rjc2.title("직업카드 등록")
            rjc2.resizable(False, False)
            rjc2.configure(background="white")
            tt = k, "번째 분의 직업 카드를 등록 해 주세요."
            text5 = tkinter.Label(rjc2, text=tt, font=font, background="white")
            text5.pack()

            temp_id = None
            pool = ThreadPool(processes=1)
            async_result = pool.apply_async(rfid)
            # t = threading.Thread(target=rfid, args=(temp_id))
            # t.start()

            # temp_id = rfid()
            temp_id = async_result.get()
            print(temp_id)

            if (temp_id != None):
                temp[k] = temp_id
                text4 = tkinter.Label(rjc2, text=temp[k], font=font, background="white")
                text4.pack()
                rjc2.destroy()
                temp_id = None

        text2 = tkinter.Label(rjc, text=temp, font=font, background="white")
        text2.pack()
        btn22 = Button(rjc, command=rolling_dice, background="#c8e6ee")
        btn22.config(text='다음으로 진행', font=font)
        btn22.pack()
        btn22.place(x=330, y=480)

    t = threading.Thread(target=defi)
    t.start()


def rfid():
    print("rfid read s")
    time.sleep(5)
    reader = SimpleMFRC522()
    id, text = reader.read()
    print(id)
    GPIO.cleanup()
    print("rfid read e")
    return id
    # return 1


def find_job(temp):
    global crrt_job
    for i in job:
        if i['uid'] == temp:
            name = i['job']
            str = i['health']
            strr = i['stress']
            p = i[drinkP]
            n = i[drinkN]
            crrt_job.pd.DataFrame(data=[[name, str, strr, p, n]],
                                  columns=["name", "str", "strr", "h", "bh"])  # 체력 스트레스 호 불호


toplevel.geometry("1024x600+0+0")
toplevel.title("코딩이랑 유관합니다! - 관교폴리")

toplevel.resizable(False, False)
toplevel.configure(background="white")

image1 = PhotoImage(file="버튼기본.png")
btn1 = Button(toplevel, command=opening, background="white", relief='flat')
btn1.config(image=image1)
btn1.pack()

btn1.place(x=360, y=130)

toplevel.mainloop()