# - coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random


#�{�[�h�̔ԍ��Őݒ�(�ڂŌ��Đ�������)
GPIO.setmode(GPIO.BOARD)

#LED��`
LD1 = 19
LD2 = 21
LD3 = 23
LD4 = 27
#LED�̃|�[�g�錾
GPIO.setup(LD1, GPIO.OUT)
GPIO.setup(LD2, GPIO.OUT)
GPIO.setup(LD3, GPIO.OUT)
GPIO.setup(LD4, GPIO.OUT)

#SW��`
SW1 = 31
SW2 = 33
SW3 = 35
SW4 = 37
#SW�̃|�[�g�錾
GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#�X�s�[�J�[��`
SP = 40
#�X�s�[�J�[�̃|�[�g�錾
GPIO.setup(SP, GPIO.OUT)

#LED�̔z��?
#LEDs = ["LD1", "LD2", "LD3", "LD4"]
LEDs = [19, 21, 23, 27]

def Lit(gpioNo) :
    GPIO.output(gpioNo, GPIO.HIGH)
    time.sleep(1.0)
    GPIO.output(gpioNo, GPIO.LOW)


if __name__ == '__main__'

    print("programm start\n")
    try:
        while true:
            for i in range(0, 10) :
                LitNo = random.choice(LEDs)
                Lit(LitNo)
    except KeyboardInterrupt :
        print("detect key interrupt\n")
    finally:
        GPIO.cleanup()
        print("program exit\n")
