# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random

#ボードの番号で設定(目で見て数えるやつ)
GPIO.setmode(GPIO.BOARD)

#スイッチとかLEDとかの配列
LEDs  = [19, 21, 23, 27]
SWCHs = [31, 33, 35, 37]
SPKR  = [40]

#すべてのGPIO番号を格納するやーつ
GPIOs = LEDs + SWCHs + SPKR

#LED定義
LD0 = LEDs[0]
LD1 = LEDs[1]
LD2 = LEDs[2]
LD3 = LEDs[3]

#LEDステータス用の変数
status_LEDs = [False, False, False, False]

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
SW0 = SWCHs[0]
SW1 = SWCHs[1]
SW2 = SWCHs[2]
SW3 = SWCHs[3]
#SWのポート宣言
GPIO.setup(SW0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#スピーカー定義
SP = SPKR[0]
#スピーカーのポート宣言
GPIO.setup(SP, GPIO.OUT)

#PWMインスタンス生成
Bell = GPIO.PWM(SP, 30)

#平均(しかも切り上げ)律音階周波数
mel_C = 262 #ド
mel_Cu= 277 #ド#
mel_D = 294 #レ
mel_E = 330 #ミ
mel_F = 349 #ファ
mel_G = 392 #ソ
mel_A = 440 #ラ
mel_B = 494 #シ

#インターバル用のリスト[s]
wait_times0 = [0.70, 1.0, 1.5, 2.0]
#光ってる時間のリスト[ms]
wait_times1 = [250, 500, 700, 900]

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

    HitBell()   #ヒットした時の楽譜を鳴らす
    Hits += 1   #ヒット回数をインクリメント
#    print("Hit func end")

#LEDの状態を更新する関数
def UpdateLED():
#    print("UpdateLED func start")
    for i in range(0, 4):   #4回繰り返す
        GPIO.output(LEDs[i], status_LEDs[i])    #LEDの状態を1つずつ更新
#    print("UpdateLED func end")

#LEDを(すべて)消灯させる関数
def dark_led():
    print("dark_led")
    global status_LEDs

    status_LEDs = [False, False, False, False]  #LEDのステータス全部0V
    UpdateLED() #LEDの状態を更新

#ゲームが始まった時にLEDを光らせる関数
#LEDが一つづつ左に流れて右に流れていく
def brink_LED_line():
#    print("brink_LED_line func start")
    global status_LEDs

    for i in range(0, 4):
        status_LEDs[i] = True
        UpdateLED()
        sleep(0.1)
        status_LEDs[i] = False 
        UpdateLED()

    time.sleep(0.1)

    for i in range(3, -1):
        status_LEDs[i] = True
        UpdateLED()
        sleep(0.1)
        status_LEDs[i] = False 
        UpdateLED()
#多分ここ全部で0.9秒強消費されてる
#    print("brink_LED_line func end")

#当たり判定
def is_hit(self):   #ダウンエッジの時にしか呼ばれないし,多分全長押しは効かない
#    print("is_hit func start")
    global status_LEDs

    if ((status_LEDs[0] and not GPIO.input(SWCHs[0])) or
        (status_LEDs[1] and not GPIO.input(SWCHs[1])) or
        (status_LEDs[2] and not GPIO.input(SWCHs[2])) or
        (status_LEDs[3] and not GPIO.input(SWCHs[3])) ): #光らせてるLEDに対応したスイッチが押されてたらヒット!   
        Hit()       #ヒット関数呼び出し
    elif (not (GPIO.input(SW0) and GPIO.input(SW1)) or
          not (GPIO.input(SW1) and GPIO.input(SW2)) or
          not (GPIO.input(SW2) and GPIO.input(SW3)) or
          not (GPIO.input(SW3) and GPIO.input(SW0))): #全押し回避
        MissBell()
        MissBell()
        
    dark_led()  #全部のLEDを消灯
#    print("is_hit func end")

#イベント削除用
def remove_events():
    print("rmove_events")
    global SWCHs

    for i in range(0, 4):   #4回繰り返す
        GPIO.remove_event_detect(SWCHs[i])  #SW0~SW3の割り込み関数を除去

#イベント追加用(ゲーム用のボタン割込認識のための関数)
def add_events():
    print("add_events")
    global SWCHs

    for i in range(0, 4):   #4回繰り返す
        GPIO.add_event_detect(SWCHs[i], GPIO.FALLING, is_hit, 100)  #SW0~SW3まで割り込み関数を付与

#ゲーム始める時の関数 LEDの初期化 割り込みイベントの追加 ヒット回数の初期化
def game_start_set():
    print("game_start_set")
    global Hits

    add_events()    #スイッチの割り込み関数を呼ぶ
    dark_led()      #LEDをすべて消す
    StartBell() #ゲームスタートの楽譜を鳴らす
    Hits = 0    #ヒット数を初期化

#ゲームが終わった時に呼ばれる ヒット数で音が変わる
def game_over():
    print("game_over")
    global Hits

    if (Hits > 7):  #ゲームクリア条件
        YahooBell() #達成していたらクリア楽譜を鳴らす
    else :  #条件を満たしていなかったら
        for i in range(3):  #三回
            MissBell()  #ミス譜面を鳴らす

#プログラム終了の際GPIOを解除
def cleanup_GPIOs():
    print "cleanup_GPIOs"
    Bell.stop() #スピーカーのインスタンスを削除
#    GPIO.cleanup(GPIOs)    #GPIOsの番号すべてを占有解除
    for i in GPIOs: #GPIOsの中身を捜査してその番号を
        GPIO.cleanup(i) #GPIO番号の占有解除

if __name__ == "__main__":
    try:
        while True: #無限ループ
            print("program start")            
            remove_events() #スイッチの割り込み関数削除

            for i in range(0, 10000):   #1000秒まってその間に
                if (GPIO.event_detected(SW0) and
                    GPIO.input(SW0) == False):  #SW0が押してすぐ離せばゲームスタート
                    break;
                time.sleep(0.1)

           time.sleep(0.9)   #もし一秒(上の0.1秒を通過した後にこっちに来るから足して1秒)
            if (GPIO.input(SW0) == False):  #長押ししていたら
                break   #ゲーム終了
            
            game_start_set()    #ゲームを開始するための処理を行う
            time.sleep(1)   #フェイントの1秒止まる

            for i in range(0, Loop):    #Loop回繰り返す
                randTime = random.choice(wait_times1)   #wait_times1秒後に光らす
                status_LEDs[random.randint(0, 3)] = True    #LEDの状態を発光へ
                UpdateLED() #LEDの状態を更新

                for j in range(1, randTime):    #randTime[ms]光る
                    if (GPIO.event_detected(SW0) or
                        GPIO.event_detected(SW1) or
                        GPIO.event_detected(SW2) or
                        GPIO.event_detected(SW3)):  #が押されたら
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
