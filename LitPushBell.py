# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

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

#�f���[�e�B�[�T�C�N����`
DC = 50
#����(�������؂�グ)�����K���g�� C D E ��`
mel_C = 262 #�h
mel_D = 294 #��
mel_E = 330 #�~

#PWM�C���X�^���X����
BELL = GPIO.PWM(SP, 30)
BELL.start(50)

points = 0

def Lit(gpioNo, status)
    GPIO.output(gpioNo, status)

def HitBell()
    Bell.ChangeFrequency(mel_C)
    time.sleep(50)
    Bell.ChangeFrequency(mel_D)
    time.sleep(50)
    Bell.ChangeFrequency(mel_E)
    time.sleep(50)
    Bell.ChangeFreauency(0)

def MissBell()
    Bell.ChangeFrequency(100)
    time.sleep(50)
    Bell.ChangeFrequency(100)
    time.sleep(100)
    Bell.ChangeFrequency(0)

print("programm start\n")
try:
    while true:
        for i in range(0, 10):
            for j in range(1, 500):
                if (GPIO.input(SW1) and GPIO.input(SW2) and GPIO.input(SW3) and GPIO.input(SW4)):
                        MissBell()
                        MissBell()
                        break
                if (GPIO.input(SW1)):
                        HitBell()
                        break
                else:
                    Lit(LD1, true)
                    time.sleep(2)
                if (j == 499):
                    MissBell()

            Lit(LD1, false)
            sleep(1000)

except KeyboardInterrupt:
    print("detect key interrupt\n")

finally:
    BELL.stop()
    GPIO.cleanup()
    print("program exit\n")
