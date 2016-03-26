import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def event_callback1(self):
    print 'event_callback1'
def event_callback2(self):
    print 'event_callback2'

GPIO.add_event_detect(37, GPIO.FALLING, event_callback1, 100)
#GPIO.add_event_callback(37, event_callback1)

GPIO.add_event_detect(35, GPIO.FALLING, event_callback2, 100)
#GPIO.add_event_callback(35, event_callback2)

if __name__ == "__main__":
    print('GPIO Version', GPIO.VERSION)

    try:
        while True:
            time.sleep(1)
    except:
        print("keyboard interrupt")
    finally:
        GPIO.cleanup()
