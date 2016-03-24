# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random

#ボードの番号で設定(目で見て数えるやつ)
GPIO.setmode(GPIO.BOARD)

#LED定義
LD0 = 19
LD1 = 21
LD2 = 23
LD3 = 27
#LEDのポート宣言
GPIO.setup(LD0, GPIO.OUT)
GPIO.setup(LD1, GPIO.OUT)
GPIO.setup(LD2, GPIO.OUT)
GPIO.setup(LD3, GPIO.OUT)
#LED消灯
GPIO.output(LD0, GPIO.LOW)
GPIO.output(LD1, GPIO.LOW)
GPIO.output(LD2, GPIO.LOW)
GPIO.output(LD3, GPIO.LOW)

#SW定義
SW0 = 31
SW1 = 33
SW2 = 35
SW3 = 37
#SWのポート宣言
GPIO.setup(SW0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#スピーカー定義
SP = 40
#スピーカーのポート宣言
GPIO.setup(SP, GPIO.OUT)

#PWMインスタンス生成
BELL = GPIO.PWM(SP, 30)
BELL.start(50) #デューティーサイクル50%固定
BELL.stop()

#平均(しかも切り上げ)律音階周波数
mel_C = 262 #ド
mel_D = 294 #レ
mel_E = 330 #ミ
mel_F = 349 #ファ
mel_G = 392 #ソ
mel_A = 440 #ラ
mel_B = 494 #シ

#LEDステータス用の変数
status_LD = [False, False, False, False]

#時間ランダム用の時間
wait_times0 = [0.800, 1.000, 1.200, 1.500]
wait_times1 = [0.300, 0.400, 0.500, 0.600]
#LEDランダム用の変数
LEDs = [19, 21, 23, 27]

#成功回数
Hits = 0
#全体ループ用
Loop = 10

def Lit(gpioNo)
    GPIO.output(gpioNo, True)

def Dark(gpioNo)
    GPIO.output(gpioNO, False)

def HitBell()
    Bell.start(0.05)
    Bell.ChangeFrequency(mel_C)
    time.sleep(0.05)
    Bell.ChangeFrequency(mel_D)
    time.sleep(0.05)
    Bell.ChangeFrequency(mel_E)
    time.sleep(0.05)
    Bell.stop()

def MissBell()
    Bell.start(50)
    Bell.ChangeFrequency(100)
    time.sleep(0.05)
    Bell.stop()

def Hit()
    HitBell()
    Hits += 1

def UpdateLED()
    for i in range (0, 4):
        GPIO.output(LEDs[i], status_LED[i])

if __name__ == '__main__'
    print("programm start\n")
    try:
        while true:
            for i in range(0, Loop):
                randTIME = rand.choice(wait_times1)

                for j in range(1, randTime):
                    #LEDをランダムに光らせる処理を書いてくだちい
                    randLED = random.randint(0,3)
                    status_LED[randLED] = True
                    UpdateLED()

                    if (j == randTime - 1):
                        MissBell()
                    elif (GPIO.input(SW0) and GPIO.input(SW1) and GPIO.input(SW2) and GPIO.input(SW3)):
                        MissBell()
                        MissBell()
                        MissBell()
                        break

                    elif ((status_LD[0] and GPIO.input(SW1)) or 
                          (status_LD[1] and GPIO.input(SW2)) or 
                          (status_LD[2] and GPIO.input(SW3)) or 
                          (status_LD[3] and GPIO.input(SW4))):
                        Hit()
                        break

                    else:
                        MissBell()
                        time.sleep(0.002)

                status_LED[randLED] = False
                UpdateLED()
                randTIME = rand.choice(wait_times0)
                sleep(randTIME)

    except KeyboardInterrupt:
        print("detect key interrupt\n")

    finally:
        BELL.stop()
        GPIO.cleanup()
        print("program exit\n")
