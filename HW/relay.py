import RPi.GPIO as GPIO
import time

# GPIO 및 릴레이 핀 설정
GPIO.setmode(GPIO.BCM)
relay_pin = 18
GPIO.setup(relay_pin, GPIO.OUT)

# 라벨에 따른 동작 수행 함수
def perform_action_based_on_label(label):
    steps_per_revolution = 128
    steps_per_revolution1 = 256

    if label == 'vinyl':
        # 릴레이 작동
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(1.5)
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(2)

    elif label == 'plastic':
        # 릴레이 작동
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(3.5)
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(2)

    elif label == 'can':
        # 릴레이 작동
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(4)
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(2)

    elif label == 'general':
        # 릴레이 작동
        GPIO.output(relay_pin, GPIO.HIGH)
        time.sleep(4)
        GPIO.output(relay_pin, GPIO.LOW)
        time.sleep(1)
