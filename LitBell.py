# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

#ボードの番号で設定(目で見て数えるやつ)
GPIO.setmode(GPIO.BOARD)

#LED定義
LD1 = 19
LD2 = 21
LD3 = 23
LD4 = 27
#LEDのポート宣言
GPIO.setup(LD1, GPIO.OUT)
GPIO.setup(LD2, GPIO.OUT)
GPIO.setup(LD3, GPIO.OUT)
GPIO.setup(LD4, GPIO.OUT)

#SW定義
SW1 = 31
SW2 = 33
SW3 = 35
SW4 = 37
#SWのポート宣言
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#スピーカー定義
SP = 40
#スピーカーのポート宣言
GPIO.setup(SP, GPIO.OUT)

#デューティーサイクル定義
DC = 50
#平均(しかも切り上げ)律音階周波数 C D E 定義
mel_C = 262 #ド
mel_D = 294 #レ
mel_E = 330 #ミ

#PWMインスタンス生成
BELL = GPIO.PWM(SP, 30)
BELL.start(50)

status = false

print("programm start\n")
try:
    while true:
        if (not GPIO.input(SW1)):
            Bell.ChangeFrequency(mel_D)
        if (not GPIO.input(SW2)):
            Bell.ChangeFrequency(mel_C)
        if (not GPIO.input(SW3)):
            Bell.ChangeFrequency(mel_E)
        if (not GPIO.input(SW4)):
           Bell.ChangeFrequency(0) 
        else :
           Bell.ChangeFrequency(0)

except KeyboardInterrupt:
    print("detect key interrupt\n")

finally:
    BELL.stop()
    GPIO.cleanup()
    print("program exit\n")
