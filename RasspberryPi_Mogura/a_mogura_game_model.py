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
#Bell.start(50) #デューティーサイクル50%
#Bell.stop()

#平均(しかも切り上げ)律音階周波数
mel_C = 262 #ド
mel_Cu= 277 #ド#
mel_D = 294 #レ
mel_E = 330 #ミ
mel_F = 349 #ファ
mel_G = 392 #ソ
mel_A = 440 #ラ
mel_B = 494 #シ

#LEDステータス用の変数
status_LD = False

#インターバル用のリスト[s]
wait_times0 = [0.70, 1.0, 1.5, 2.0]
#光ってる時間のリスト[ms]
wait_times1 = [250, 500, 700, 900]
#LEDランダム用の変数
LEDs = [19]

#成功回数
Hits = 0
#全体ループ用
Loop = 10

#ゲームスタートのときの楽譜
def StartBell():
#    print("StartBell func")
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
    Bell.ChangeFrequency(mel_C * 8)
    time.sleep(0.5)
    Bell.stop()

#もぐらがヒットしたときの楽譜
def HitBell():
#    print("Hit!")
    print(Hits)
    Bell.start(50)
    Bell.ChangeFrequency(mel_C * 2)
    time.sleep(0.15)
    Bell.ChangeFrequency(mel_D * 2)
    time.sleep(0.15)
    Bell.ChangeFrequency(mel_E * 3)
    time.sleep(0.15)
    Bell.stop()

#もぐらをヒットできなかったときの楽譜
def MissBell():
#    print("Miss!")
    print(Hits)
    Bell.start(50)
    Bell.ChangeFrequency(130)
    time.sleep(0.5)
    Bell.stop()

#クリアした時の楽譜(よろこびの歌のつもり)
def YahooBell():
#    print("clear!")
    time.sleep(0.1)
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
#    print("Hit func start")
    global Hits
    HitBell()
    Hits += 1
#    print("Hit func end")

#LEDの状態を更新する関数
def UpdateLED():
#    print("UpdateLED func start")
    GPIO.output(LD0, status_LD)
#    print("UpdateLED func end")

#LEDを(すべて)消灯させる関数
def dark_led():
    print("dark_led")
    global status_LD
    status_LD = False
    UpdateLED()

#ゲームが始まった時にLEDを光らせる関数
def start_brink():
#    print("start_brinc func start")
    status_LD = True
    UpdateLED()
    sleep(0.1)
    status_LD = False 
    UpdateLED()
#    print("start_brink func end")

#当たり判定
def is_hit(self):
#    print("is_hit func start")
    global status_LD
    if (status_LD and not GPIO.input(SW0)): #光らせてるLEDに対応したスイッチが押されてたらヒット!   
        status_LD = False   #LEDの状態を消灯へ
        UpdateLED() #LEDの状態を更新
        Hit()
#    print("is_hit func end")

#イベント削除用
def remove_events():
    print("rmove_events")
    global SW0
    GPIO.remove_event_detect(SW0)

#イベント追加用(ゲーム用のボタン割込認識のための関数)
def add_events():
    print("add_events")
    global SW0
    GPIO.add_event_detect(SW0, GPIO.FALLING, is_hit, 100)

#ゲーム始める時の関数 LEDの初期化 割り込みイベントの追加 ヒット回数の初期化
def game_start_set():
    print("game_start_set")
    global Hits
    add_events()
    dark_led()
    StartBell() #ゲームスタートの楽譜を鳴らす
    Hits = 0    #ヒット数を初期化

#ゲームが終わった時に呼ばれる ヒット数で音が変わる
def game_over():
    print("game_over")
    global Hits
    if (Hits > 7):  #ゲームクリア条件
        YahooBell() #達成していたらクリア楽譜を鳴らす
    else :  #条件を満たしていなかったら
        for i in range(3):
            MissBell()  #ミス譜面を鳴らす

#プログラム終了の際GPIOを解除
def cleanup_GPIOs():
    print "cleanup_GPIOs"
    Bell.stop()
    GPIO.cleanup(LD0)
    GPIO.cleanup(SW0)
    GPIO.cleanup(SP)

if __name__ == "__main__":
    try:
        while True: #無限ループ
            print("program start")            
            remove_events()

            for i in range(0, 10000):
                if (GPIO.input(SW0) == False):
                    break;
                time.sleep(0.1)

            time.sleep(1)
            if (GPIO.input(SW0) == False):
                break
            
            game_start_set()
            time.sleep(1)   #1秒止まる

            for i in range(0, Loop):    #Loop回繰り返す
                randTime = random.choice(wait_times1)   #wait_times1秒後に光らせる
                status_LD = True    #LEDの状態を発光へ
                UpdateLED() #LEDの状態を更新

                for j in range(1, randTime):    #randTime[ms]光る
                    if (GPIO.input(SW0) == False):
                        break
                    elif (j == randTime - 2): #最後まで押せなかったらミス
                        dark_led()
                        MissBell()  #ミスした楽譜を鳴らす
                        break

                    time.sleep(0.001)   #1msの遅延を与える,randTime回積み重なるので#randTime秒の出来事となる
                time.sleep(random.choice(wait_times0))    #ランダムにインターバル発生

            game_over()
            time.sleep(0.1)#スリープ入れないとオーバーヘッドの関係でプログラムが落ちる
            
    except Exception as e:#もっぱらキーボードインタラプト（C-c)用
        print e

    finally:
        cleanup_GPIOs()
        print("program exit")
