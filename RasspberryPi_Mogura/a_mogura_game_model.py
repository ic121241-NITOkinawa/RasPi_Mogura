# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random

#ボードの番号で設定(目で見て数えるやつ)
GPIO.setmode(GPIO.BOARD)

#LED定義
LD0 = 19
#LEDのポート宣言
GPIO.setup(LD0, GPIO.OUT)
#LED消灯
GPIO.output(LD0, GPIO.LOW)

#SW定義
SW0 = 37
#SWのポート宣言
GPIO.setup(SW0, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#スピーカー定義
SP = 40
#スピーカーのポート宣言
GPIO.setup(SP, GPIO.OUT)

#PWMインスタンス生成
Bell = GPIO.PWM(SP, 30)
Bell.start(50) #デューティーサイクル50%
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
status_LD = False

#長押し対策用の変数
hold_sw0 = [True, True]  #プルアップなのでこれはOFF, OFF

#インターバル用のリスト[s]
wait_times0 = [0.70, 1.00, 1.50, 1.80]
#光ってる時間のリスト[ms]
wait_times1 = [500, 700, 900, 1200]
#LEDランダム用の変数
LEDs = [19]

#成功回数
Hits = 0
#全体ループ用
Loop = 10

#ゲームスタートのときの楽譜
def StartBell():
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

#もぐらをヒットできなかったときの楽譜
def MissBell():
    print("Miss!")
    print(Hits)
    Bell.start(50)
    Bell.ChangeFrequency(130)
    time.sleep(0.5)
    Bell.stop()

#クリアした時の楽譜(よろこびの歌のつもり)
def YahooBell():
    print("clear!")
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
    
#もぐらがヒットした時の関数
def Hit():
    global Hits
    HitBell()
    Hits += 1

#LEDの状態を更新する関数
def UpdateLED():
    print("UpdateLED")
    GPIO.output(LD0, status_LD)

def start_brink():
    status_LD = True
    UpdateLED()
    sleep(0.1)
    status_LD = False 
    UpdateLED()

def is_hit():
    print("is_hit func")
    if (status_LD and (not GPIO.input(SW0))): #光らせてるLEDに対応したスイッチが押されてたらヒット!   
        status_LD = False   #LEDの状態を消灯へ
        UpdateLED() #LEDの状態を更新
        Hit()
        break

if __name__ == "__main__":
    print("programm start\n")
    try:
        while True: #無限ループ
            GPIO.remove_event_detect(LD0)

            while True:
                start_brink()
                if (GPIO.input(SW0)):
                    break

            GPIO.add_event_detect(LD0, GPIO.FALLNG, is_hit, 100)
            status_LD = False
            UpdateLED()
            StartBell() #ゲームスタートの楽譜を鳴らす
            Hits = 0    #ヒット数を初期化
            time.sleep(1)   #1秒止まる

            for i in range(0, Loop):    #Loop回繰り返す
                randTime = random.choice(wait_times1)   #wait_times1秒後に光らせる
                status_LD = True    #LEDの状態を発光へ
                UpdateLED() #LEDの状態を更新

                for j in range(1, randTime):    #randTime[ms]光る
                    if (j == randTime - 2): #最後まで押せなかったらミス
                        status_LD = False   #LEDの状態を消灯へ
                        UpdateLED() #LEDの状態を更新
                        MissBell()  #ミスした楽譜を鳴らす
                        break

                    time.sleep(0.001)   #1msの遅延を与える,randTime回積み重なるので
                                        #randTime秒の出来事となる
                randTIME = random.choice(wait_times0)   #インターバルをランダムに決める
                time.sleep(randTIME)    #インターバル発生

            #Loop回光終わった後にクリアかどうか判定される
            if (Hits > 7):  #ゲームクリア条件
                YahooBell() #達成していたらクリア楽譜を鳴らす
            else :  #条件を満たしていなかったら
                MissBell()  #ミス譜面を鳴らす
                MissBell()  #ミス譜面を鳴らす

            time.sleep(0.1)#スリープ入れないとオーバーヘッドの関係でプログラムが落ちる
            
    except:#もっぱらキーボードインタラプト（C-c)用
        print("detect key interrupt\n")

    finally:
        Bell.stop()
        GPIO.cleanup(LD0)
        GPIO.cleanup(SW0)
        GPIO.cleanup(SP)
        print("program exit\n")
