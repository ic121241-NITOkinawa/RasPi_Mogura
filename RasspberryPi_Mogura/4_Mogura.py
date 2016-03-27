# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random

#ボードの番号で設定(目で見て数えるやつ)
GPIO.setmode(GPIO.BOARD)

#すべてのGPIO番号を格納するやーつ
GPIOs = [19, 21, 23, 27, 31, 33, 35, 37, 40]

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

#スピーカーのポート定義
SP = 40
#スピーカーのポート宣言
GPIO.setup(SP, GPIO.OUT)

#PWMインスタンス生成
Bell = GPIO.PWM(SP, 30)
Bell.start(50) #デューティーサイクル50%固定
Bell.stop()

#平均(しかも切り上げ)律音階周波数
mel_C = 262 #ド
mel_D = 294 #レ
mel_E = 330 #ミ
mel_F = 349 #ファ
mel_G = 392 #ソ
mel_A = 440 #ラ
mel_B = 494 #シ

#LEDステータス用の変数
status_LED = [False, False, False, False]

#時間ランダム用の時間
wait_times0 = [0.700, 1.000, 1.500, 1.800]
wait_times1 = [500, 700, 900, 1200]
#LEDランダム用の変数
LEDs = [19, 21, 23, 27]

#成功回数
Hits = 0
#全体ループ用
Loop = 10


#ゲームスタートのときの楽譜
def StartBell():
    print("Game Start")
    Bell.start(50)
    Bell.ChangeFrequency(mel_C * 4)
    time.sleep(0.2)
    Bell.stop()
    time.sleep(0.2)
    Bell.start(50)
    Bell.ChangeFrequency(mel_C * 4)
    time.sleep(0.2)
    Bell.stop()
    time.sleep(0.2)
    Bell.start(20)
    Bell.ChangeFrequency(mel_C * 6)
    time.sleep(0.5)
    Bell.stop()
    
#もぐらがヒットしたときの楽譜
def HitBell():
    print("Hit!")
    print(Hits)
    Bell.start(50)
    Bell.ChangeFrequency(mel_C * 2)
    time.sleep(0.25)
    Bell.ChangeFrequency(mel_D * 2)
    time.sleep(0.25)
    Bell.ChangeFrequency(mel_E * 3)
    time.sleep(0.25)
    Bell.stop()

#もぐらをヒットできなかった時の音楽
def MissBell():
    print("Miss")
    print(Hits)
    Bell.start(50)
    Bell.ChangeFrequency(100)
    time.sleep(0.05)
    Bell.stop()
    time.sleep(0.05)
    Bell.start(50)
    Bell.ChangeFrequency(100)
    time.sleep(0.05)
    Bell.stop()

#クリアした時の楽譜(よろこびの歌のつもり)
def YahooBell():
    print("Game Clear!")
    Bell.start(50)
    Bell.ChangeFrequency(mel_E * 2)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_E * 2)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_F * 3)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_G * 3)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_G * 2)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_F * 2)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_E * 3)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_D * 3)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_C * 3)
    time.sleep(0.3)
    Bell.ChangeFrequency(mel_C * 3)
    time.sleep(0.3)
    Bell.stop()
    
#もぐらがヒットした時の処理
def Hit():
    print("Hit")
    global Hits
    HitBell()
    Hits += 1
    
#LEDの状態を更新する関数
def UpdateLED():
    for i in range (0, 4):
        GPIO.output(LEDs[i], status_LED[i])

if __name__ == '__main__':
    print("programm start\n")
    try:
        #無限ループ
        while True:
            status_LD = [False, False, False, False]
            UpdateLED()#LEDどもの状態をすべて消灯

            StartBell()#ゲームスタートの楽譜を鳴らす

            Hits = 0    #ヒット数を初期化
            time.sleep(1)   #1秒止まる 

            for i in range(0, Loop):
                randTime = rand.choice(wait_times1) #wait_times1[s]後に光る
                
                randLED = random.randint(0,3)
                status_LED[randLED] = True
                UpdateLED()

                for j in range(1, randTime):
                    if (j == randTime - 2): #最後まで押せなかったらミスとみなす
                        MissBell()

                    elif (GPIO.input(SW0) and GPIO.input(SW1) and GPIO.input(SW2) and GPIO.input(SW3)): #全押し回避
                        MissBell()
                        MissBell()
                        break

                    elif ((status_LD[0] and GPIO.input(SW1)) or 
                          (status_LD[1] and GPIO.input(SW2)) or 
                          (status_LD[2] and GPIO.input(SW3)) or 
                          (status_LD[3] and GPIO.input(SW4))):  #当たり判定
                        Hit()
                        break

                    else:
                        time.sleep(0.001)

                status_LED[randLED] = False
                UpdateLED()

                randTIME = rand.choice(wait_times0) #インターバルの時間を決める
                sleep(randTIME) #インターバル発生

                if (Hits > 0):  #ゲームクリア条件を満たせばなる
                    YahooBell()
                else:           #ゲームクリアじゃなければなる
                    MissBell()
                    MissBell()
                    MissBell()

                time.sleep(1)   #オーバーヘッドの関係で入れないと落ちる

            while True:
                if (GPIO.input(SW0) == True):
                    break
            
            if ((GPIO.input(SW0) == True) and
                (GPIO.input(SW3) == True)):
                break



    except :    #もっぱらキーボードインタラプト(C-c)用
        print("some except happend!(クソコメ)")

    finally:
        BELL.stop()
        for i in range(0, 9):
            GPIO.cleanup(i)

        print("program exit")
