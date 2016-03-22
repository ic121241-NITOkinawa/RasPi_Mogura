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
