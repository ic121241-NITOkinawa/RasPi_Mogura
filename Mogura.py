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

print("programm start\n")

try:
    while true:
        if (not GPIO.input(SW1)):
            GPIO.output(LD1, GPIO.HIGH)
        if (not GPIO.input(SW2)):
            GPIO.output(LD2, GPIO.HIGH)
        if (not GPIO.input(SW3)):
            GPIO.output(LD3, GPIO.HIGH)
        if (not GPIO.input(SW4)):
            GPIO.output(LD4, GPIO.HIGH)
        else :
            GPIO.output(LD1, GPIO.LOW)
            GPIO.output(LD2, GPIO.LOW)
            GPIO.output(LD3, GPIO.LOW)
            GPIO.output(LD4, GPIO.LOW)
except KeyboardInterrupt:
    print("detect key interrupt\n")
finally:
    GPIO.cleanup()
    print("program exit\n")
